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
                    </el-row>
                </el-col>
                <el-col :span='24'>
                      <div class="padd15">
                        <el-col :span='24' class='mgt24 fsz24px txtgreencolor'>{{currentgoods}}</el-col>
                        <el-col :span='24' class='mgt24'>基础数据</el-col>
                        <el-col :span='24' class='mgt24'>
                            <el-form ref="form" :model="requestform" label-width="80px">
                                <el-row :gutter='40'>
                                <el-col :span='10'>
                                    <el-form-item label="规格">
                                        <el-input v-model="requestform.Specs"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="请验单号">
                                        <el-input v-model="requestform.CheckNumber"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="品名/名称">
                                        <el-input v-model="requestform.Name"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="来料批号">
                                        <el-input v-model="requestform.ProductNumber"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="供货单位">
                                        <el-input v-model="requestform.Supplier"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="物料编码">
                                        <el-input v-model="requestform.Number"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="数量">
                                        <el-input v-model="requestform.Amount"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="单位">
                                        <el-input v-model="requestform.Unit"></el-input>
                                    </el-form-item>
                                </el-col>
                                </el-row>
                            </el-form>
                        </el-col>
                        <el-col :span='24' class='mgt24'>请验项目</el-col>
                        <el-col :span='24' class='mgt24'>
                            <el-form ref="form" :model="projectform" label-width="80px">
                                <el-row :gutter='40'>
                                <el-col :span='10'>
                                    <el-form-item label="请验工序" class="PuNo">
                                        <el-select v-model="projectform.CheckProcedure" placeholder="请选择请验工序">
                                            <el-option label="工序一" value="1"></el-option>
                                            <el-option label="工序二" value="2"></el-option>
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="请验部门">
                                        <el-input v-model="projectform.CheckDepartment"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="申请时间">
                                        <el-date-picker
                                            v-model="projectform.CheckDate"
                                            type="date"
                                            placeholder="选择日期">
                                        </el-date-picker>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="请验人">
                                        <el-input v-model="projectform.CheckUser"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="备注">
                                        <el-input type="textarea" v-model="projectform.Comment"></el-input>
                                    </el-form-item>
                                </el-col>
                                </el-row>
                            </el-form>
                        </el-col>
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