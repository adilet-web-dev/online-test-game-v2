import TestList from "@/views/test/TestList.vue";
import TestDetail from "@/views/test/TestDetail.vue";
import TestCreate from "@/views/test/TestCreate.vue";
import {isAuthenticated} from "@/services/auth.service";

import {redirectIfNotAuthentication} from "@/router";
import TestEdit from "@/views/test/TestEdit.vue";

export default [
    {
        path: '/tests',
        name: 'testList',
        component: TestList,
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