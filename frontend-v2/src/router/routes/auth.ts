import Login from "@/views/auth/Login.vue";
import Signup from "@/views/auth/Signup.vue";

export default [
    {
        path: '/login',
        name: 'login',
        component: Login
    },
    {
        path: '/signup/:uuid',
        name: 'signup',
        component: Signup
    }

]