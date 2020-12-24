<template>
    <el-row :gutter='20'>
        <el-col :span='24' class="mgt24 container" v-show="showstep">
            <div class="mgb24 fsz14px">当前批次流程</div>
            <el-steps :active="currentstep" finish-status="success">
                <el-step class="cursor" name='description' v-for="(item,index) in batchinfo" :key='index' :title="item.Status" >
                    <template slot="description">
                        <div><span>姓名：</span><span>{{item.User}}</span></div>
                        <div><span>时间：</span><span>{{item.OperationTime}}</span></div>
                    </template>
                </el-step>
            </el-steps>
        </el-col>
        <el-col :span='24'>
            <el-row class="container mgt24">
                <el-col :span='24'>
                   <el-row>
                    <el-col :span='3' class="mgr15 boxshadow">
                        <el-select v-model="searchObj.category" placeholder="品名">
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
                     <el-col :span='2' class="boxshadow req">
                        <el-button type='primary' @click="SearchTab">查询</el-button>
                    </el-col>
            </el-row>
                </el-col>
                <el-col :span='24' class="mgt24">
                        <div class="mgt24 boxshadow">
                          <el-table
                            :data="batchTableData.data"
                            size='small'
                            highlight-current-row
                            style="width: 100%"
                            @row-click="handletabClick">
                            <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                            <el-table-column
                                fixed="right"
                                label="操作"
                                width="100">
                                <template slot-scope="scope">
                                    <el-button @click="handleClick(scope.row)" type="text" size="small">查看详情</el-button>
                                </template>
                            </el-table-column>
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
           currentstep:3,
           batchinfo:[],
           showstep:false,
            searchObj:{
               category:'丹参',
               registrydate:moment(new Date()).format('YYYY-MM-DD'),
               state:'待审核',
           },
            options: [{
                value: '选项1',
                label: '物料一'
                }],
            opstate: [{
                value: '请验审核',
                label: '请验审核'
                }, {
                value: '取样',
                label: '取样'
                },{
                value: '接收',
                label: '接收'
                }],
            batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchtableconfig:[{prop:'Specs',label:"规格"},{prop:'CheckNumber',label:'请验单号'},{prop:'Name',label:'品名'},{prop:'ProductNumber',label:'来料批号'},{prop:'Supplier',label:'供货单位'},{prop:'Number',label:'物料编码'},{prop:'Amount',label:'数量'},{prop:'Unit',label:'单位'},{prop:'CheckDate',label:'请验时间'}],//批次列表
        }
    },
    created(){
        this.getInitTab()
        this.getSelectOption()
    },
    methods: {
        handletabClick(row){
            this.getCurrentSteps(row.CheckProjectNO)
        },
        getCurrentSteps(CheckProjectNO){
           var params={
                Action:'p',
                CheckProjectNO:CheckProjectNO
            }
            this.axios.get('/lims/Board',{params:params}).then((res) => {
                if(res.data.code=='1000'){
                    this.batchinfo=res.data.data
                    if(this.batchinfo.length!==[]){
                        this.showstep=true
                    }else{
                        this.showstep=false
                    }
                }else{
                    this.$message({
                        type:'info',
                        message:'获取数据失败，请重试'
                    })
                }
            })
        },
        handleClick(row){
        },
         getSelectOption() { //获取下拉列表选项
           this.axios.get('/lims/AllProduct').then((res) => {
               if(res.data.code=='1000'){
                  this.options=res.data.data.map((item) => {
                      return {
                          value:item,
                          label:item
                      }
                  })
               }

           })
        },
        SearchTab(){ //查询相关数据
            var params={
                Page:this.batchTableData.offset,
                PerPage:this.batchTableData.limit,
                Product:this.searchObj.category,
                DateTime:moment(this.searchObj.registrydate).format("YYYY-MM-DD"),
                Status:this.searchObj.state
            }
            this.axios.get('/lims/CheckForm',{params:params}).then((res) => {
                if(res.data.data.length==0){
                    this.showstep=false
                }
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        getInitTab(){ //初始化获取表格数据
            var params={
                Page:this.batchTableData.offset,
                PerPage:this.batchTableData.limit,
                Product:this.searchObj.category,
                DateTime:this.searchObj.registrydate,
                Status:this.searchObj.state
            }
            this.axios.get('/lims/CheckForm',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.SearchTab()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.SearchTab()
        }
    },
}
</script>
<style scoped>

</style>