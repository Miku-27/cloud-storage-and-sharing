document.addEventListener('alpine:init',()=>{

    Alpine.data('pageManager',()=>({

        init(){
            console.log("Alpine init!")
            this.getUserFile()
        },

        ProfileDropdownOpen:false,
        openFilePicker(){
            this.$refs.fileInput.click()
        },

        filesToUpload:[],
        onFileSelect(e){
            const files = e.target.files
            if (!files || files.length === 0) return

            console.log(files)
            this.filesToUpload.push(files[0]);
            this.uploadFiles();
        },
        
        sidebarExpanded:false,
        currentView:'dashboard',
        dbTab:'files',

        shTab:"withme",

        filesList: [
            {
                id: 11,
                name: 'Presentation_Draft.pptx',
                type: 'SLIDES',
                size: '9.8 MB',
                updatedAt: 'Updated 2 weeks ago'
            },
            {
                id: 12,
                name: 'Deepak.pptx',
                type: 'SLIDES',
                size: '93.38 MB',
                updatedAt: 'Updated 21/2/2005'
            }
        ],

        collectionsList: [
            { id: 'C1', title: 'Product_Assets', count: 14 },
            { id: 'C2', title: 'Marketing', count: 8 },
        ],

        sharedWithMe: [
            {
                id: 1,
                name: 'Marketing_Kit_2026',
                meta: 'Incoming // Collection',
                owner: 'Sarah.OS'
            },
            {
                id: 2,
                name: 'Design_Assets.zip',
                meta: 'Incoming // File',
                owner: 'Design.Team'
            }
        ],
        
        sharedByMe: [
            {
                id: 3,
                name: 'Sprint_Report.xlsx',
                meta: 'Outgoing // File',
                owner: 'You'
            }
        ],

        toggleSidebar(){
            this.sidebarExpanded=!this.sidebarExpanded
        },

        progressTracker(progressPercent){
            console.log(progressPercent)
        },


        calculateSize(bytes){
            const sizes = ["Bytes","KB","MB","GB"];
            const k = 1024;
            const i = Math.floor(Math.log(bytes)/Math.log(k));
            const value = bytes/Math.pow(k,i).toFixed(2);
        
            return `${value} ${sizes[i]}`
        },

        async getUserFile(){
            let [status,data] = await requestBackend("/api/user/me/files","GET");
            if (!status){
                return;
            }
            data.files.forEach(file => {
                file.updatedAt = "Updated At: "+new Date(file.updatedAt).toLocaleDateString();
                file.size = this.calculateSize(file.size)
            });
            this.filesList = data.files;
        },

        async getUploadUrl(payload){
            let [status,data] = await requestBackend("api/file",'POST',payload)
            if (!status){
                return;
            }

            return data
        },

        isUploading:false,
        async uploadFiles(){
            if (this.isUploading===true){return;}
            this.isUploading=true;
            while(this.filesToUpload.length > 0){
                const file = this.filesToUpload.shift();
                const payload = {
                    file_name:file.name,
                    file_size:file.size,
                    mime_type:file.type
                }

                const link_data = await this.getUploadUrl(payload);
                result = await uploadFileToCloud(file,link_data,(p)=>this.progressTracker(p))
                if (result.success){
                    let [status,data] = await requestBackend(`api/file/${link_data.file_key}`,'PATCH',{'status':'success'})
                    if (!status){
                        return;
                    }
                    this.filesList.push({
                        "id":link_data.file_key,
                        "name":file.name,
                        "type":file.type,
                        "size":file.size,
                    })
                }
            }
            this.isUploading=false;
        },
    }))
})