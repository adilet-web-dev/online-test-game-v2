import TestList from "@/views/test/TestList.vue";
import UserTestList from "@/views/test/UserTestList";
import TestDetail from "@/views/test/TestDetail.vue";
import TestCreate from "@/views/test/TestCreate.vue";


import {redirectIfNotAuthentication} from "@/router";
import TestEdit from "@/views/test/TestEdit.vue";

export default [
    {
        path: '/tests',
        name: 'test list',
        component: TestList,
        beforeEnter: redirectIfNotAuthentication
    },
    {
        path: '/tests/my',
        name: 'user test list',
        component: UserTestList,
        beforeEnter: redirectIfNotAuthentication
    },
    {
        path: '/tests/:id',
        name: 'test detail',
        component: TestDetail,
        beforeEnter: redirectIfNotAuthentication
    },
    {
        path: '/tests/create',
        name: 'test create',
        component: TestCreate,
        beforeEnter: redirectIfNotAuthentication
    },
    {
        path: '/tests/:id/edit',
        name: 'test edit',
        component: TestEdit,
        beforeEnter: redirectIfNotAuthentication
    }

]