<template>
    <el-row class="container mgt24">
        <el-row>
            <el-col :span='3' class="mgr15 boxshadow">
               <el-select v-model="searchObj.category" placeholder="物料类">
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :span='3' class="mgr15 boxshadow">
               <el-select v-model="searchObj.state" placeholder="状态">
                    <el-option
                    v-for="item in opstate"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value">
                    </el-option>
                </el-select>
            </el-col>
            <el-col :span='3' class="mgr15 boxshadow">
               <el-date-picker
                v-model="searchObj.registrydate"
                type="date"
                placeholder="选择日期">
               </el-date-picker>
            </el-col>
            <el-col :span='3' class="boxshadow req">
                <el-button type='primary' @click="SearchTab">查询</el-button>
            </el-col>
        </el-row>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){

        return {
           searchObj:{
               category:'巴戟胶囊',
               registrydate:moment(new Date()).format('YYYY-MM-DD')
           },
            options: [{
                value: '选项1',
                label: '物料一'
                }],
            batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            opstate: [{
                value: '待审核',
                label: '待审核'
                }, {
                value: '待取样',
                label: '待取样'
                },{
                value: '待检验',
                label: '待检验'
                },{
                value: '检验中',
                label: '检验中'
                },{
                value: '已完成',
                label: '已完成'
                }],
        }
    },
    methods: {
        SearchTab() {
            console.log(123)       
        }
    },
}
</script>
<style scoped>

</style>