import {playerEvents, creatorEvents} from "@/services/events";
import {Settings, Player, Test} from "@/services/interfaces";
import {HOST} from "../../hosts";


const WS_DOMAIN: string = `ws://${HOST}`;
const ServerWebSocket = require('ws');

const TESTING = false;

class BaseWebsocketService {

    protected ws!: WebSocket;

    protected async connect(url: string): Promise<boolean> {

        const self = this;


        // since the connection is established for a long time,
        // every 0.1 second it is checked that the connection is established,
        // if yes, then the promise will return true
        return new Promise<boolean>((resolve, reject) => {

            if (TESTING){
                this.ws = new ServerWebSocket(url);
            } else {
                this.ws = new WebSocket(url);
                this.ws.onerror = function() {
                    reject("couldn't connect")
                }
            }

            let intervalId: any = null;
            const func = () => {
                if (self.ws.readyState) {
                    clearInterval(intervalId);
                    resolve(true);
                }
            };
            intervalId = setInterval(func, 100);
        });
    }

    public send(data: object){
        this.ws.send(JSON.stringify(data));
    }

    public setMessageEvent(func: Function){
        this.ws.onmessage = function (message) {
            func(message);
        }
    }

    public closeConnection() {
        this.ws.close();
    }

}

class CreatorWS extends BaseWebsocketService{
    async connectToRoom(roomId: number): Promise<boolean> {
        return await super.connect(`${WS_DOMAIN}/ws/cubes/${roomId}/creator`);
    }

    sendPlayers(players: object[]) {
        this.send({
            event: creatorEvents.SEND_PLAYERS,
            players: players
        });
    }

    informPlayersToStartTheGame() {
        this.send({
            event: creatorEvents.START_GAME
        })
    }

    sendSettings(settings: Settings){
        this.send({
            event: creatorEvents.SEND_SETTINGS,
            settings: settings
        })
    }

    sendQuestion(question: object) {
        this.send({
            event: creatorEvents.SEND_QUESTION,
            question: question
        })
    }
    
    sendWinnersAndFinish(winners: Player[]){
        this.send({
            event: creatorEvents.FINISH_GAME,
            winners: winners
        })
    }

    sendTestAnswers(test: Test){
        this.send({
            event: creatorEvents.SEND_TEST_ANSWERS,
            test: test
        })
    }

}

class PlayerWS extends BaseWebsocketService{
    async joinToRoom(roomId: number, name: string) {

        let connected: boolean = await super.connect(`${WS_DOMAIN}/ws/cubes/${roomId}/player`);
        let self = this;
        if (connected){
            self.send({event: playerEvents.JOIN_PLAYER, name: name});
        }
    }

    sendAnswer(player: Player){
        this.send({event: playerEvents.SEND_ANSWER, player: player});
    }

}


export {CreatorWS, PlayerWS, WS_DOMAIN};
