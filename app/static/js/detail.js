document.addEventListener('alpine:init', () => {
    Alpine.data('detailManager', () => ({
        fileData: {
            name: 'Draft_v1.docx',
            type: 'Microsoft Word Document',
            size: '84 KB',
            fileId: '0x2441',
            createdAt: 'Oct 12, 2025 // 14:20',
            updatedAt: '2 mins ago',
        },

        userList: [
            { id: 1, name: 'Sarah.OS',email:"hello@gmail.com", role: 'Owner', color: 'bg-orange-200' },
            { id: 2, name: 'Marcus_V',email:"hello@gmail.com", role: 'Editor', color: 'bg-blue-200' },
            { id: 3, name: 'Sarah.OS',email:"hello@gmail.com", role: 'Owner', color: 'bg-orange-200' },
        ],

        targetUser:'',
        currentUserPage:1,
        totalUserPages:3,
        showShareModal: false,
        showRevokeModal:false,
        userToRevoke:{
            'name':'',
            'id':''
        },
        userToSearch:null,
        showRenameModal:false,
        newFileName:'',
        showDeleteModal:false,
        linkGenerated: false,
        generatedUrl: '',
        copyText: 'Copy to Clipboard',
        shareForm: { expiry: '7', password: '' },

        grantMode:false,
        searchQuery:null,

        foundUsers:[],

        resetShareModal() {
            this.showShareModal = true;
            this.linkGenerated = false;
            this.copyText = 'Copy to Clipboard';
        },
        
        copyToClipboard() {
            navigator.clipboard.writeText(this.generatedUrl);
            this.copyText = 'URL COPIED';
            setTimeout(() => this.copyText = 'Copy to Clipboard', 2000);
        },

        newName:null,
        async deleteFile(){
            let [status,data] = await requestBackend(`/api/file/${this.fileId}`,'DELETE')
            if (!status){
                return;
            }
        },
        async renameFile(){
            let [status,data] = await requestBackend(`/api/file/${this.fileId}`,'PATCH',{'fileName':this.newName})
            if (!status){
                return;
            }
        },
        async downloadFile() {
            let [status,data] = await requestBackend(`/api/file/${this.fileId}`,'GET')
            if (!status){
                return;
            }
            window.location.href = data;
        },
        async generateShareLink(){
            let [status,data] = await requestBackend(`/api/file/${this.fileId}`,'GET')
            if (!status){
                return;
            }
            this.generatedUrl = `https://aura.os/s/${token}`;
            this.linkGenerated = true;
        },
        async getUserWithAccess(){
            const params = new URLSearchParams({
                email: this.userToSearch,
                page: 1,
                limit: 3
            });
            let [status,data] = await requestBackend(`/api/file/${this.fileId}/users?${params}`,'GET')
            if (!status){
                return;
            }
            this.userList=data;
        },

        openRevokeModal(user){
            this.showRevokeModal=true;
            this.userToRevoke=user;
        },
        async revokeAccess(){
            let [status,data] = await requestBackend(`/api/file/${this.fileId}/users?${params}`,'DELETE',{'user_id':this.userToRevoke.id})
            if (!status){
                return;
            }
            this.userList = this.userList.filter(user => user.id !== this.userToRevoke.id)
        }
        
    }));
});

