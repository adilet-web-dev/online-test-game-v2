import axios from 'axios';
import {Test} from "@/services/interfaces";
import {authHeader} from "@/services/auth.service";
import {HOST} from "../../hosts";


const DOMAIN: string = `http://${HOST}`;

export class ApiService {

    public async obtainRoomId() {

        const response = await axios.get(
            DOMAIN + '/api/v1/rooms/obtain_room/',
            {headers: {'Authorization': authHeader()}}
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
            {headers: {'Authorization': authHeader()}}
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
                {headers: {'Authorization': authHeader()}}
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
        const response = await axios.post(
            DOMAIN + '/api/v1/tests/',
            test,
            {headers: {'Authorization': authHeader()}}
        );
        return {
            status: response.status
        }
    }

    public async updateTest(test: Test, testId: number){
        const response = await axios.put(
            DOMAIN + '/api/v1/tests/' + testId,
            test
        )
    }

    public async getTestList() {
        let data =  {
            status: 0,
            tests: [],
        };

        try{
            const response = await axios.get(
                DOMAIN + '/api/v1/tests/',
                {headers: {'Authorization': authHeader()}}
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

}
