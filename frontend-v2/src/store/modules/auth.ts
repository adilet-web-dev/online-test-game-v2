import { Mutation, State } from 'vuex-simple';

const token = sessionStorage.getItem('token');
const initialState = token
    ? { loggedIn: true, token: token }
    : { loggedIn: false, token: null };


export class Authentication {
    @State()
    public state: {loggedIn: boolean, token: string | null};

    constructor() {
        this.state = initialState;
    }

    @Mutation()
    public updateToken(newToken: string){
        this.state.token = newToken;
    }

    @Mutation()
    public logIn(){
        this.state.loggedIn = true;
    }


}