document.addEventListener('alpine:init', () => {
    Alpine.data('registerManager', () => ({
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
        isLoading: false,
        showPassword: false,

        async handleRegister() {
            
            if (this.password !== this.confirmPassword) {
                alert("Passwords do not match.");
                return;
            }

            this.isLoading = true;
            
            const payload = {
                username: this.username,
                email: this.email,
                password: this.password
            };
            
            let [status,data] = await requestBackend("/api/auth/user","POST",payload);
            if (status == true){
                window.location.href = 'login';
            }
            else{
                this.isLoading=false;
            }
        }
    }));
});