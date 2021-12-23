import axios from "axios";
import {HOST} from "../../hosts";

const DOMAIN: string = `http://${HOST}`;

import {app} from "@/main";

interface User {
    username: string,
    password: string
}

export function authHeader(){

    app.$cookies?.isKey("token");
    if (app.$cookies?.isKey("token")) {
        let token = app.$cookies?.get("token");
        return 'Bearer ' + token;
    } else {
        return ''
    }
}

export function isAuthenticated(){
    return app.$cookies?.isKey("token");
}

export class AuthService {
    isLoggedIn(): boolean{
        return <boolean>app.$cookies?.isKey("token");
    }

    async login(user: User){

        try {
            let response = await axios.post(DOMAIN + '/api/token/', {
                username: user.username,
                password: user.password
            });

            app.$cookies?.set('token', response.data.access);

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

    async logout(){
        sessionStorage.removeItem('token');
    }


}
