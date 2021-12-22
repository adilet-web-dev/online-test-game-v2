export interface Player {
    name: string,
    score: number
}

export interface Settings {
    maxTime: number,
    bonus: boolean,
    showAnswers: boolean
}


// WARNING: this is same as backend model fields
export interface Option {
    answer: string,
    is_true: boolean
}

export interface Question {
    title: string,
    options: Option[]
}

export interface Test {
    name: string,
    questions: Question[]
}
