// store/store.ts

import { Module, State } from 'vuex-simple';
import { Authentication } from './modules/auth';

export class MyStore {

    @Module()
    public auth = new Authentication();

    @State()
    public version = "2.0.0";
}

