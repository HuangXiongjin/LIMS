<template>
    <el-row :gutter='20'>
        <el-col :span='24' class="mgt24">
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
        <el-col :span='24' class="mgt24 container">
            <div class="mgb24 fsz14px">当前批次流程</div>
            <el-steps :active="currentstep" finish-status="success">
                <el-step class="cursor" name='description' v-for="(item,index) in batchinfo" :key='index' :title="item.Status" >
                    <template slot="description" v-if='item.User'>
                        <div><span>姓名：</span><span>{{item.User}}</span></div>
                        <div><span>时间：</span><span>{{item.OperationTime}}</span></div>
                    </template>
                </el-step>
            </el-steps>
        </el-col>
        <el-col :span='24' class="mgt24">
            <div class="container">
                <el-menu :default-active="'1'" class="bgwhite" mode="horizontal" @select="handleSelect">
                    <el-menu-item :index="'1'" style="height:46px;lineHeight:30px;">申请列表</el-menu-item>
                    <el-menu-item :index="'2'" style="height:46px;lineHeight:30px;">通过列表</el-menu-item>
                </el-menu>
                <div class="mgt24" v-if="currentChoose==='1'">
                    <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%"
                    @selection-change="handleSelectionChange"
                    @row-click='clickAllTab'>
                    <el-table-column type="selection" width="55"></el-table-column>
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                    <el-table-column
                        fixed="right"
                        label="操作"
                        width="100">
                        <template slot-scope="scope">
                            <el-button @click="handlePass(scope.row)" type="text" size="small" class="bledit">通过</el-button>
                            <el-button @click.native.prevent="handleBack(scope.row)" type="text" size="small" class="redde">驳回</el-button>
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
                    <div style="textAlign:right;" class="mgt24" v-if="IsDoing">
                        <el-button type="danger" size='small'>驳回</el-button>
                        <el-button type="success" size='small' @click="mulBatchPass">批量审核通过</el-button>
                    </div>
                </div>
                  <div class="mgt24" v-if="currentChoose==='2'">
                    <el-table
                    :data="batchTableData2.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%"
                    @row-click='clickSingleTab'>
                    <el-table-column v-for="item in batchtableconfig2" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
                    </el-table>
                    <div class="paginationClass">
                        <el-pagination background  layout="total, prev, pager, next, jumper"
                        :total="batchTableData2.total"
                        :current-page="batchTableData2.offset"
                        :page-size="batchTableData2.limit"
                        @size-change="handleSizeChange2"
                        @current-change="handleCurrentChange2">
                        </el-pagination>
                    </div>
                </div>
            </div>
        </el-col>
    </el-row>
</template>
<script>
var moment =require('moment')
export default {
    data(){

        return {
           IsDoing:JSON.parse(sessionStorage.getItem('Rights').replace(/'/g, '"')).includes("请验审核"),
           currentstep:1,
           batchinfo:[{Status:'申请'},{Status:'请验审核'},{Status:'取样'},{Status:'接收'},{Status:'分发'},{Status:'质检'},{Status:'报告'},{Status:'质检审核'},{Status:'放行'}],
           checkedRow:[],
           searchObj:{
               category:'玉米淀粉',
               registrydate:moment(new Date()).format('YYYY-MM-DD'),
               state:'请验审核',

           },
            options: [{
                value: '选项1',
                label: '物料一'
                }],
            opstate: [{value: '申请',label: '申请'},{value: '请验审核',label: '请验审核'},{value: '取样',label: '取样'},{value: '接收',label: '接收'},{value: '分发',label: '分发'},
            {value: '质检',label: '质检'},{value: '报告',label: '报告'},{value: '质检审核',label: '质检审核'},{value: '放行',label: '放行'}],
            currentChoose:'1',
            batchTableData:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchTableData2:{ //物料BOM
                data:[],
                limit: 5,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            CheckProjectNO:'',
            batchtableconfig:[{prop:'Specs',label:"规格"},{prop:'CheckNumber',label:'请验单号'},{prop:'Name',label:'品名'},{prop:'ProductNumber',label:'来料批号'},{prop:'Supplier',label:'供货单位'},{prop:'Number',label:'物料编码'},{prop:'Amount',label:'数量'},{prop:'Unit',label:'单位'},{prop:'CheckDate',label:'请验时间',width:'200'}],//批次列表
            batchtableconfig2:[{prop:'Specs',label:"规格"},{prop:'CheckNumber',label:'请验单号'},{prop:'Product',label:'品名'},{prop:'ProductNumber',label:'来料批号'},{prop:'Supplier',label:'供货单位'},{prop:'Number',label:'物料编码'},{prop:'ProductType',label:'物料类型'},{prop:'Amount',label:'数量'},{prop:'Unit',label:'单位'},{prop:'OperationTime',label:'操作时间',width:'200'}],//批次列表
        }
    },
    created(){
        this.SearchTab()
        this.getSelectOption()
    },
    methods: {
        clickSingleTab(row){
            this.getCurrentSteps(row.No)    
        },
        clickAllTab(row){
            this.getCurrentSteps(row.CheckProjectNO)
        },
        getCurrentSteps(CheckProjectNO){
           var params={
                Action:'p',
                CheckProjectNO:CheckProjectNO
            }
            this.axios.get('/lims/Board',{params:params}).then((res) => {
                if(res.data.code=='1000'){
                    this.currentstep=res.data.data.length
                    this.batchinfo=this.batchinfo.map((item) => { //清空缓存的状态
                       return {Status:item.Status}
                   })
                   this.batchinfo.splice(0,res.data.data.length)
                   this.batchinfo=res.data.data.concat(this.batchinfo)
                }else{
                    this.$message({
                        type:'info',
                        message:'获取数据失败，请重试'
                    })
                }
            })
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
        SearchTab(){
            var params={
                Page:this.batchTableData.offset,
                PerPage:this.batchTableData.limit,
                Product:this.searchObj.category,
                DateTime:moment(this.searchObj.registrydate).format("YYYY-MM-DD"),
                Status:this.searchObj.state
            }
            this.axios.get('/lims/CheckForm',{params:params}).then((res) => {
                this.batchTableData.data=res.data.data
                this.batchTableData.total=res.data.total
            })
        },
        getPassedTab(){
            var params={
                Page:this.batchTableData2.offset,
                PerPage:this.batchTableData2.limit,
                Name:localStorage.getItem('Name')
            }
            this.axios.get('/lims/CheckLog',{params:params}).then((res) => {
                this.batchTableData2.data=res.data.data
                this.batchTableData2.total=res.data.total
            })
        },
        mulBatchPass(){ //多条数据审核通过
            if(this.checkedRow.length==0){
                this.$message({
                    type:'error',
                    message:'请选勾选要通过的数据'
                })
            }else{
                this.$confirm('此操作将审核通过该项, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
                }).then(() => {
                  var arr=this.checkedRow.map((item) => {
                      return item.CheckProjectNO
                  })
                  var params={
                   CheckProjectNO:JSON.stringify(arr),
                   DateTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
                   VerifyName:localStorage.getItem('Name')
            }
            this.axios.post('/lims/CheckVerify',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                      type: 'success',
                      message: '审核通过!'
                    });
                    this.SearchTab()
                }
            })  
                }).catch(() => {
                    this.$message({
                      type: 'info',
                      message: '已取消审核'
                    });   
                })
                }
        },
        handleSelectionChange(row){ //选择多条数据
            this.checkedRow=row
        },
        handleBack(row){ //驳回审核
            console.log(row)
        },
        handlePass(row){ //通过审核
            this.$confirm('此操作将审核通过该项, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
            }).then(() => {
                var params={
                   CheckProjectNO:JSON.stringify([row.CheckProjectNO]),
                   DateTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
                   VerifyName:localStorage.getItem('Name')
            }
            this.axios.post('/lims/CheckVerify',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                      type: 'success',
                      message: '审核通过!'
                    });
                    this.SearchTab()
                }
            })
            }).catch(() => {
            this.$message({
                type: 'info',
                message: '已取消审核'
            });          
            });
        },
        handleSelect(key) {
            if(key==2){
                this.getPassedTab()
            }
            this.currentChoose=key
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.SearchTab()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.SearchTab()
        },
        handleSizeChange2(limit){ //每页条数切换
            this.batchTableData2.limit = limit
            this.getPassedTab()
      },
        handleCurrentChange2(offset) { // 页码切换
            this.batchTableData2.offset = offset
            this.getPassedTab()
        }
    },
}
</script>
<style scoped>

</style>