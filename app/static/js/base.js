async function requestBackend(url,method,dataToSend=null,contentType='application/json'){ 
    const csrfToken = getCookie('csrf_token');

    const options = {
        method: method,
        headers: {
            'Content-Type': contentType,
            'X-CSRF-TOKEN': csrfToken
        }
    };

    if (dataToSend) {
        options.body = JSON.stringify(dataToSend);
    }
    
    try {
        const httpResponse = await fetch(url, options);
        response = await httpResponse.json()
        
        // unauthorized check not needed as it is checked in backend and redirect to
        // if (httpResponse.status === 401) {
        //     window.dispatchEvent(new CustomEvent('show-toast', { 
        //         detail: {
        //             message: response.msg,
        //             type: response.success
        //         }     
        //     }));
        //     setTimeout(() => {
        //         window.location.href = "/login";
        //     }, 2000);
        // }
        
        //some data is being send likefetching request so no toast msg
        if (httpResponse.ok && response.success === true && response.data != null){
            return [true,response.data];
        }
        //if no data is send then toast message
        else if(response.success === true && response.data == null){
            window.dispatchEvent(new CustomEvent('show-toast', { 
                detail: {
                    message: response.msg,
                    type: response.success
                }     
            }));
            return [true,null];
        }
        //if no data and and failire toast mesg red
        else{
            window.dispatchEvent(new CustomEvent('show-toast', { 
                detail: {
                    message: response.msg,
                    type: response.success
                }  
            }));
            return [false,null];
        }
        
    } catch (error) {
        console.error("Network or Setup Error:", error);
        window.dispatchEvent(new CustomEvent('show-toast', { 
            detail: {
                message: "Network error, Please try again!",
                type: false
            }  
        }));
        return [false,null];
    }
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function uploadFileToCloud(file,urlData,onProgressCallback){
    return new Promise((resolve,reject) => {
        try{
            const xhr = new XMLHttpRequest();
            console.log("inside upload",file,urlData)
            
            xhr.open('PUT',urlData.upload_url);
        
            xhr.onload = () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    resolve({ success: true, error: null });
                } else {
                    resolve({success: false,status: xhr.status});
                }
            };

            xhr.onerror = () => {
                resolve({ success: false, status: 0});
            };

            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percent = Math.round((event.loaded / event.total) * 100);
                    
                    if (onProgressCallback) {
                        onProgressCallback(percent);
                    }
                }
            };
            
            xhr.send(file)

        }catch(err){
            resolve({success: false,status: err.message});
        }
    });
} 

function customToastMessage(message,success){
    window.dispatchEvent(new CustomEvent('show-toast', { 
        detail: {
            message: message,
            type: success
        }     
    }));
}
