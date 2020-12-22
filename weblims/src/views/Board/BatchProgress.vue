<template>
    <el-row :gutter='20'>
        <el-col :span='7'>
            <div class="container mgt24" style="height:400px;">
                <el-col :span='24' style="borderBottom:1px solid #ccc;" class="padd15">
                    <span class="fontWet titl" style="display:inline-block;height:40px;lineHeight:36px;">批次列表</span>
                </el-col>
                <el-col :span='24' class="mgt24">
                    <el-table
                        :data="batchTableData.data"
                        size='small'
                        highlight-current-row
                        style="width: 100%"
                        @row-click="handletabClick">
                        <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                    </el-table>
                </el-col>
            </div>
        </el-col>
        <el-col :span='17'>
            <el-row class="container mgt24">
                <el-col :span='24'>
                    123
                </el-col>
            </el-row>
        </el-col>
               
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
            batchTableData:{ //物料BOM
                data:[],
                limit: 3,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchtableconfig:[{prop:'Name',label:'样本品名'},{prop:'ProductNumber',label:'来料批号'},{prop:'VerifyDate',label:'检验时间',width:155}],//批次列表
        }
    },
    created(){
     
    },
    methods: {
        handletabClick(row){
            console.log(row)
        }
        },
}
</script>
<style scoped>

</style>