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

        onFileSelect(e){
            const file = e.target.files
            if (!files || files.length === 0) return

            this.file = files[0]
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

        async getUserFile(){
            let [status,data] = await requestBackend("/api/user/me/files","GET");
            this.filesList = data.files;
        }
    }))
})