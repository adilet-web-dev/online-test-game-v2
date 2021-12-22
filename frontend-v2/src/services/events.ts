export const playerEvents = {
    // api events
    AUTHENTICATE: 'authenticate',
    // ws events
    UPDATE_PLAYERS: 'update players',
    JOIN_PLAYER: 'join player',
    SEND_ANSWER: 'send answer',
    GET_QUESTION: 'get question',

};

export const creatorEvents = {
    // api events
    AUTHENTICATE: 'authenticate',
    GET_TEST_QUESTIONS: 'get questions',
    GET_TESTS: 'get tests',
    // ws events
    SEND_PLAYERS: 'send player',
    SEND_SETTINGS: 'send settings',
    NEXT_QUESTION: 'next question',
    SEND_QUESTION: 'send question',
    GET_ANSWER: 'get answer',
    START_GAME: 'start game',
    FINISH_GAME: 'finish game',
    SEND_TEST_ANSWERS: 'send test answers'
};

export const otherEvents = {
    NOT_AUTHENTICATED: '401',
};


