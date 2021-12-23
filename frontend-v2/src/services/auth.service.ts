import axios from "axios";
import {HOST} from "../../hosts";

const DOMAIN: string = `http://${HOST}`;

import {app} from "@/main";

interface User {
    username: string,
    password: string
}

export function authHeader(){

    if (sessionStorage.hasOwnProperty("token")) {
        let token = sessionStorage.getItem('token');
        return 'Bearer ' + token;
    } else {
        return ''
    }
}

export function isAuthenticated(){
    return sessionStorage.hasOwnProperty("token");
}

export class AuthService {
    isLoggedIn(): boolean{
        return sessionStorage.hasOwnProperty("token");
    }

    async login(user: User){

        try {
            let response = await axios.post(DOMAIN + '/api/token/', {
                username: user.username,
                password: user.password
            });
            sessionStorage.setItem('token', response.data.access);

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
