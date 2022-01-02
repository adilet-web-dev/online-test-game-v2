import axios from 'axios';
import {Test} from "@/services/interfaces";
import {AuthService} from "@/services/auth.service";
import {HOST} from "../../hosts";

let auth_service = new AuthService();


const DOMAIN: string = `http://${HOST}`;

export class ApiService {

    public async obtainRoomId() {

        const response = await axios.get(
            DOMAIN + '/api/v1/rooms/obtain_room/',
            {headers: {'Authorization': auth_service.authHeader()}}
        );
        return {
            status: response.status,
            room_id: response.data.room_id,
        };

    }

    public async closeRoom(roomId: number) {

        const response = await axios.post(
            DOMAIN + '/api/v1/rooms/close_room/',
            {"room_id": roomId},
            {headers: {'Authorization': auth_service.authHeader()}}
        );
        return {
            status: response.status,
            room_id: response.data.room_id,
        };

    }

    public async getTest(testId: number | string) {
        try {
            const response = await axios.get(
                DOMAIN + '/api/v1/tests/' + testId,
                {headers: {'Authorization': auth_service.authHeader()}}
            );

            return {
                status: response.status,
                test: response.data,
            };

        } catch (e) {
            return {
                status: e.response.status,
                test: []
            }
        }


    }

    public async createTest(test: Test){

        try {
            const response = await axios.post(
                DOMAIN + '/api/v1/tests/',
                test,
                {headers: {'Authorization': auth_service.authHeader()}}
            );
            return {
                status: response.status
            }
        } catch (e) {
            if (e.response != undefined){
                // even if it's error but server has responded and it has a status
                return {status: e.response.status};
            } else {
                return {status: 405} // server error
            }
        }

    }

    public async updateTest(test: Test, testId: number){
        const response = await axios.put(
            DOMAIN + '/api/v1/tests/' + testId,
            test
        )
    }

    public async getTestList(url = '/api/v1/tests/') {
        let data =  {
            status: 0,
            tests: [],
        };

        try{

            const response = await axios.get(
                DOMAIN + url,
                {headers: {'Authorization': auth_service.authHeader()}}
            );
            data.status = response.status;
            data.tests = response.data;
        } catch (e) {
            if (e.response != undefined){
                // even if it's error but server has responded and it has a status
                data.status = e.response.status;
            } else {
                data.status = 405 // server error
            }

        }

        return data;

    }

    public async getUserTestList(){
        return this.getTestList('/api/v1/tests/get_user_tests/');
    }

    public async checkTestOwner(id: number): Promise<boolean> {
        const response = await axios.get(
            DOMAIN + '/api/v1/tests/check_owner/' + id,
            {headers: {'Authorization': auth_service.authHeader()}}
        )

        return response.data;
    }

}
