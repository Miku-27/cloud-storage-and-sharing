document.addEventListener('alpine:init', () => {
    Alpine.data('authManager', () => ({
        
        email: '',
        password: '',
        isLoading: false,
        showPassword:false,

        async handleLogin() {
            this.isLoading = true;
            const payload = {
                email:this.email,
                password:this.password
            };

            let [status,data] = await requestBackend("/api/auth/token","POST",payload);
            if (status == true){
                window.location.href = '/';
            }
            else{
                this.isLoading=false;
            }
        }
    }));
});