document.addEventListener('alpine:init',()=>{

    Alpine.data('pageManager',()=>({

        init(){
            console.log("Alpine init!")
        },

        sidebarExpanded:false,
        currentView:'dashboard',
        dbTab:'files',

        shTab:"withme",

        filesList: [
            {
                id: 1,
                name: 'Draft_v1.docx',
                type: 'DOCX',
                size: '84 KB',
                updatedAt: 'Updated 2h ago'
            },
            {
                id: 2,
                name: 'Design.fig',
                type: 'FIG',
                size: '2.1 MB',
                updatedAt: 'Updated yesterday'
            },
            {
                id: 3,
                name: 'Notes.txt',
                type: 'TXT',
                size: '12 KB',
                updatedAt: 'Updated 3 days ago'
            },
            {
                id: 4,
                name: 'Neural_Weights.bin',
                type: 'DATA',
                size: '842 MB',
                updatedAt: 'Updated 5 mins ago'
            },
            {
                id: 5,
                name: 'Q3_Growth_Strategy.pdf',
                type: 'PDF',
                size: '4.2 MB',
                updatedAt: 'Updated 1 hour ago'
            },
            {
                id: 6,
                name: 'Interface_v2_Final.sketch',
                type: 'SKETCH',
                size: '114 MB',
                updatedAt: 'Updated 6 hours ago'
            },
            {
                id: 7,
                name: 'System_Audit.log',
                type: 'LOG',
                size: '128 KB',
                updatedAt: 'Updated yesterday'
            },
            {
                id: 8,
                name: 'Archive_2024.tar.gz',
                type: 'ZIP',
                size: '2.1 GB',
                updatedAt: 'Updated 2 days ago'
            },
            {
                id: 9,
                name: 'Main_Protocol.cpp',
                type: 'CODE',
                size: '42 KB',
                updatedAt: 'Updated 4 days ago'
            },
            {
                id: 10,
                name: 'Brand_Assets.ai',
                type: 'VECTOR',
                size: '18.5 MB',
                updatedAt: 'Updated 1 week ago'
            },
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
        }
    }))
})