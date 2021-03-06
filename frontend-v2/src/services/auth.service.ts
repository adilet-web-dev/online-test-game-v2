import axios from "axios";
import {HOST} from "../../hosts";

const DOMAIN: string = `http://${HOST}`;

import {app} from "@/main";
import {Vue} from "vue-property-decorator";

interface User {
    username: string,
    password: string
}


export class AuthService extends Vue{
    authHeader(){

        if (this.$cookies.isKey("token")) {
            let token = this.$cookies.get("token");
            return 'Bearer ' + token;
        } else {
            return ''
        }
    }

    isAuthenticated(){
        return this.$cookies.isKey("token");
    }

    async login(user: User){

        try {
            let response = await axios.post(DOMAIN + '/api/token/', {
                username: user.username,
                password: user.password
            });

            let expireIn = new Date(new Date().getTime() + 3600 * 60 * 1000);

            app.$cookies?.set(
                'token',
                response.data.access,
                {expires: expireIn}
            );

            return {
                status: response.status,
                token: response.data.access
            }
        } catch (e) {
            return {
                status: e.response.status,
                token: ""
            }
        }
    }

    async signup(user: User, uuid: string){

        try {
            let response = await axios.post(DOMAIN + '/users/signup/' + uuid, {
                username: user.username,
                password: user.password
            });

            return response.status

        } catch (e) {
            return e.response.status
        }
    }

    async logout(){
        this.$cookies.remove('token');
    }

}
