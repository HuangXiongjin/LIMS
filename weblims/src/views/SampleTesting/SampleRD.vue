<template>
    <el-row :gutter='20'>
        <el-col :span='7'>
            <div class="container mgt24" style="height:400px;">
                <el-col :span='24' style="borderBottom:1px solid #ccc;" class="padd15">
                    <span class="fontWet titl" style="display:inline-block;height:40px;lineHeight:36px;">请验单号</span>
                </el-col>
                <el-col :span='24' class="mgt24">
                    <el-table
                        :data="batchTableData.data"
                        size='small'
                        highlight-current-row
                        style="width: 100%"
                        @row-click="handletabClick">
                        <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                    </el-table>
                    <div class="paginationClass">
                        <el-pagination background  layout="total, prev, pager, next, jumper"
                        :total="batchTableData.total"
                        :current-page="batchTableData.offset"
                        :page-size="batchTableData.limit"
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange">
                    </el-pagination>
                    </div>
                </el-col>
            </div>
        </el-col>
        <el-col :span='17'>
            <el-row class="container mgt24">
                <el-col :span='24'>
                    <el-row>
                        <el-col :span='4' class="mgr15 boxshadow">
                            <el-input
                                placeholder="类别/品名"
                                prefix-icon="el-icon-search"
                                v-model="searchObj.category">
                            </el-input>
                        </el-col>
                        <el-col :span='4' class="mgr15 boxshadow">
                            <el-select v-model="searchObj.goods" placeholder="物料类">
                                <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span='4' class="mgr15 boxshadow">
                           <el-select v-model="searchObj.goods" placeholder="物料类">
                                <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span='4' class="mgr15 boxshadow">
                           <el-date-picker
                            v-model="searchObj.registrydate"
                            type="date"
                            placeholder="选择日期">
                           </el-date-picker>
                        </el-col>
                        <el-col :span='5' style="height:48px;">
                          <el-radio-group v-model="operation" size='small' style="lineHeight:48px;">
                            <el-radio-button v-for="(item,index) in operations" :label="item" :key="index">{{item}}</el-radio-button>
                          </el-radio-group>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col :span='24'>
                      <div class="padd15">
                        <el-col :span='24' class='mgt24 fsz24px txtgreencolor'>{{currentgoods}}</el-col>
                        <el-col :span='24'>
                            <div style="float:right;">
                                <el-button type="success">确认接收</el-button>
                                <el-button type="info">去分发</el-button>
                            </div>
                        </el-col>
                      </div> 
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
          searchObj:{
               category:'',
               registrydate:'',
               goods:'',
           },
           operation:'',
           operations:['样本分发','记录分发'],
           currentgoods:'',
           requestform:{Specs:'',CheckNumber:'',Name:'',ProductNumber:'',Supplier:'',Number:'',Amount:'',Unit:''},
           projectform:{CheckProcedure:'',CheckDepartment:'',CheckDate:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),CheckUser:localStorage.getItem('Name'),Comment:''},
            options: [{
                value: '选项1',
                label: '物料一'
                }, {
                value: '选项2',
                label: '物料二'
                }],
            batchTableData:{ //物料BOM
                data:[
                    {CheckNumber:'BJKFY',Name:'巴戟口服液',CheckDate:moment(new Date()).format('YYYY-MM-DD HH:mm:ss')},
                    {CheckNumber:'PTTKFY',Name:'葡萄糖口服液',CheckDate:moment(new Date()).format('YYYY-MM-DD HH:mm:ss')},
                    {CheckNumber:'KFY',Name:'口服液',CheckDate:moment(new Date()).format('YYYY-MM-DD HH:mm:ss')},
                    ],
                limit: 10,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchtableconfig:[{prop:'CheckNumber',label:'请验单号'},{prop:'Name',label:'品名'},{prop:'CheckDate',label:'请验时间'}],//批次列表
        }
    },
    created(){
       
    },
    methods: {
        handletabClick(row){ //左侧tab点击事件
            this.currentgoods=row.CheckNumber
            alert('侧边栏点击事件')
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
        },
    },
}
</script>
<style scoped>

</style>