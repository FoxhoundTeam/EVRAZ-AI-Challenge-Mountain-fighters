import Vuex from 'vuex'
import http from './http'
import Axios from 'axios'
import Vue from 'vue'

Vue.use(Vuex)


const store = new Vuex.Store({
    state: {
        user: null,
        isAuthenticated: false,
        cameras: [],
        violations: [],
        selectedCamera: {},
        camerasCount: null,
        employeesCount: null,
        violationsCount: null,
        periodType: 1,
        dates: [],
        chart: {},
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setAuthenticated(state, isAuthenticated) {
            state.isAuthenticated = isAuthenticated;
        },
        setCameras(state, cameras) {
            state.cameras = cameras;
            state.selectedCamera = cameras[0];
        },
        setSelectedCamera(state, camera) {
            state.selectedCamera = camera;
        },
        setPeriodType(state, periodType) {
            state.periodType = periodType;
        },
        setDates(state, dates) {
            state.dates = dates;
        },
        setChart(state, chart){
            state.chart = {
                datasets: [
                    {
                        label: 'Нарушения',
                        borderColor: '#f87979',
                        data: chart,
                    }
                ]
            };
        },
        setViolationsCount(state, violationsCount){
            state.violationsCount = violationsCount;
        },
        setViolations(state, violations){
            state.violations = violations;
        },
        setCameraStat(state, cameraStat) {
            state.camerasCount = cameraStat;
        },
        setEmployeeStat(state, employeeStat) {
            state.employeesCount = employeeStat;
        },
        addFrame(state, frame) {
            if (state.cameras.length) {
                let ind = state.cameras.findIndex(v => v.id == frame.camera.id)
                if (ind != -1) {
                    let camera = state.cameras[ind];
                    camera.last_frame = frame;
                    Vue.set(state.cameras, ind, camera);
                }
            }
        },
        addViolation(state, violation) {
            state.violations.unshift(violation);
        },
    },
    actions: {
        async setCameras(context) {
            let response = (await http.getList('Camera', {}, true)).data;
            context.commit('setCameras', response);
        },
        async setChart(context) {
            let filters = {dt_from: context.state.dates[0], dt_to: context.state.dates[1]};
            let response = (await http.getList('Chart', filters, true)).data;
            context.commit('setChart', response.data);
            context.commit('setViolationsCount', response.count);
        },
        async setViolations(context) {
            let filters = {dt_from: context.state.dates[0], dt_to: context.state.dates[1]};
            let response = (await http.getList('Violation', filters, true)).data;
            context.commit('setViolations', response);
        },
        async setCameraStat(context) {
            let response = (await http.getList('CameraStat', {}, true)).data;
            context.commit('setCameraStat', response.count);
        },
        async setEmployeeStat(context) {
            let response = (await http.getList('EmployeeStat', {}, true)).data;
            context.commit('setEmployeeStat', response.count);
        },
        async addItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let response = (await http.createItem(data.url, item_data, true)).data;
            let items = context.state[data.items_name]
            items.push(response);
            context.commit(mutation, items);
        },
        async updateItem(context, data) {
            let item_data = data.data
            let mutation = data.mutation;
            let dataID = data.dataID;
            let response = (await http.updateItem(data.url, dataID, item_data, true)).data;
            let items = context.state[data.items_name]
            let index = items.findIndex(v => v.id == dataID);
            if (index != -1) {
                Vue.set(items, index, response);
            }
            context.commit(mutation, items);
        },
        async login(context, creds) {
            var username = creds.username;
            var password = creds.password;
            var reg_exp_mail = /^[\w-.]+@([\w-]+\.)+[\w-]{2,4}$/
            var login_info = {
                email: username,
                password: password
            }
            if (username.match(reg_exp_mail) != null) {
                login_info = {
                    email: username,
                    password: password
                }
            } else {
                login_info = {
                    username: username,
                    password: password
                }
            }
            var status = false;
            try {
                await (Axios.post("/rest_api/auth/login/", login_info, {headers: {'X-CSRFToken': Vue.$cookies.get('csrftoken')}}));
                status = true;
            } catch (error) {
                var data = error.response.data;
                if (data.non_field_errors) {
                    Vue.showErrorModal(data.non_field_errors);
                } else {
                    var result = '';
                    for (var k in data) {
                        result += `${k}: ${data[k]}\n`
                    }
                    Vue.showErrorModal(result);
                }
            }
            await context.dispatch('checkAuth');
            return status;
        },
        async logout(context) {
            await Axios.post("/rest_api/auth/logout/", {headers: {'X-CSRFToken': Vue.$cookies.get('csrftoken')}});
            context.commit('setAuthenticated', false);
            context.commit('setUser', {});
        },
        async checkAuth(context) {
            try {
                var result = await Axios.get("/rest_api/auth/user/");
                if (result.status != 200) {
                    context.commit('setUser', {});
                    return
                }
                context.commit('setAuthenticated', true);
                context.commit('setUser', result.data);
            } catch (e) {
                context.commit('setUser', {});
            }
        },
    }
})

export default store;
