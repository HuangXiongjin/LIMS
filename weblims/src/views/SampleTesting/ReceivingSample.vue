<template>
    <el-row :gutter='20'>
        <el-col :span='24' class="mgt24 container">
            <div class="mgb24 fsz14px">当前批次流程</div>
            <el-steps :active="currentstep" finish-status="success">
                <el-step class="cursor" name='description' v-for="(item,index) in batchinfo" :key='index' :title="item.Status" >
                    <template slot="description" v-if='item.CheckUser'>
                        <div><span>姓名：</span><span>{{item.CheckUser}}</span></div>
                        <div><span>时间：</span><span>{{item.CheckDate}}</span></div>
                    </template>
                </el-step>
            </el-steps>
        </el-col>
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
                        <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
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
                           <el-select v-model="searchObj.category" placeholder="物料类">
                                <el-option
                                v-for="item in options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                                </el-option>
                            </el-select>
                        </el-col>
                        <el-col :span='4' class="mgr15 boxshadow">
                           <el-select v-model="searchObj.state" placeholder="物料类">
                                <el-option
                                v-for="item in opstate"
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
                        <el-col :span='3' class="boxshadow req">
                            <el-button type='primary' @click="SearchTab">查询</el-button>
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
                                        <el-input v-model="requestform.Product"></el-input>
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
                                <el-col :span='10'>
                                    <el-form-item label="物料类别">
                                        <el-input v-model="requestform.ProductType"></el-input>
                                    </el-form-item>
                                </el-col>
                                <el-col :span='10'>
                                    <el-form-item label="取样人">
                                        <el-input v-model="requestform.SampleUser"></el-input>
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
                                    <el-form-item label="请验工序">
                                        <el-input v-model="projectform.CheckProcedure"></el-input>
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
                                <el-button type="primary" @click="LookJbInfo">查看鉴别</el-button>
                                <el-button type="success" @click="receiveConfirm" v-if="IsDoing">确认接收</el-button>
                            </div>
                        </el-col>
                      </div> 
                </el-col>
            </el-row>
        </el-col>
        <el-dialog title="检测项详细信息展示" :visible.sync="dialogTableVisible">
            <el-collapse v-model="activeNames">
                <el-collapse-item title="性状" name="Character">
                    <div v-for="(item,index) in Characters" :key='index' class="lightgreen">{{item.value}}</div>
                </el-collapse-item>
                <el-collapse-item title="鉴别" name="Discern">
                    <div v-for="(item,index) in Discerns" :key='index' class="lightgreen">{{item.value}}</div>
                </el-collapse-item>
                <el-collapse-item title="检查" name="Inspect">
                    <div v-for="(item,index) in Inspects" :key='index' class="lightgreen">{{item.value}}</div>
                </el-collapse-item>
                <el-collapse-item title="含量测定" name="Content">
                    <div v-for="(item,index) in Contents" :key='index' class="lightgreen">{{item.value}}</div>
                </el-collapse-item>
                <el-collapse-item title="微生物限度" name="Microbe">
                    <div v-for="(item,index) in Microbes" :key='index' class="lightgreen">{{item.value}}</div>
                </el-collapse-item>
            </el-collapse>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogTableVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogTableVisible = false">确 定</el-button>
            </div>
        </el-dialog>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
           IsDoing:JSON.parse(sessionStorage.getItem('Rights').replace(/'/g, '"')).includes("样本接收"),
           currentstep:3,
           batchinfo:[{Status:'申请'},{Status:'请验审核'},{Status:'取样'},{Status:'接收'},{Status:'分发'},{Status:'质检'},{Status:'报告'},{Status:'质检审核'},{Status:'放行'}],
           activeNames:['Discern','Character','Inspect','Content','Microbe'],
           Discerns:[],
           Inspects:[],
           Characters:[],
           Contents:[],
           Microbes:[],
           dialogTableVisible:false,
           searchObj:{
               category:'玉米淀粉',
               state:'接收',
               registrydate:moment(new Date()).format('YYYY-MM-DD')
           },
          opstate: [{value: '申请',label: '申请'},{value: '请验审核',label: '请验审核'},{value: '取样',label: '取样'},{value: '接收',label: '接收'},{value: '分发',label: '分发'},
            {value: '质检',label: '质检'},{value: '报告',label: '报告'},{value: '质检审核',label: '质检审核'},{value: '放行',label: '放行'}],
           currentgoods:'物料编码',
           requestform:{Specs:'',CheckNumber:'',Name:'',ProductNumber:'',Supplier:'',Number:'',Amount:'',Unit:'', ProductType:'',SampleUser:''},
           projectform:{
               CheckProcedure:'',CheckDepartment:'',
               Comment:'',
               CheckProject:{Discern:[],Character:[],Inspect:[],Content:[],Microbe:[]}
           },
           options: [{
                value: '选项1',
                label: '物料一'
                }],
            rowCheckProjectNO:'',
            batchTableData:{ //物料BOM
                data:[],
                limit: 3,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchtableconfig:[{prop:'CheckNumber',label:'请验单号'},{prop:'Product',label:'品名'},{prop:'CheckDate',label:'请验时间',width:155}],//批次列表
        }
    },
    created(){
       this.getSelectOption()
       this.SearchTab()
    },
    methods: {
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
        receiveConfirm(){//领样确认
            this.$confirm('此操作将确认接收, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
            }).then(() => {
                var params={
                CheckProjectNO:this.requestform.CheckProjectNO,
                ReceiveUser:localStorage.getItem('Name'),
                ReceiveTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
                CheckNumber:this.requestform.CheckNumber
            }
            this.axios.post('/lims/Receive',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'确认接收'
                    })
                    this.SearchTab()
                }
            })
            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消'
                });          
                });
        },
        LookJbInfo(){
            this.dialogTableVisible=true
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
                TableName:"CheckForm",
                Query:"Accurate",
                Page:this.batchTableData.offset,
                PerPage:this.batchTableData.limit,
                QueryColumnName:"Product",
                QueryColumnValue:this.searchObj.category,
                TimeColumn:"CheckDate",
                StartTime:moment(this.searchObj.registrydate).format("YYYY-MM-DD 00:00:00"),
                EndTime:moment(this.searchObj.registrydate).format("YYYY-MM-DD 23:59:59"),
                QueryColumnName2:"Status",
                QueryColumnValue2:this.searchObj.state
            }
            this.axios.get('/lims/CRUD',{params:params}).then((res) => {
                if(res.data.code=='1000'){
                    this.batchTableData.data=res.data.data
                    this.batchTableData.total=res.data.total
                     if(this.rowCheckProjectNO!==''){
                        this.getCurrentSteps(this.rowCheckProjectNO)
                    }
                }
            })
        },
        handletabClick(row){ //左侧tab点击事件
            this.rowCheckProjectNO=row.CheckProjectNO
            this.currentgoods=row.CheckNumber
            this.requestform=row
            this.projectform=row
            this.getJbInfo(row.CheckProjectNO)
            this.getCurrentSteps(row.CheckProjectNO)
        },
        getJbInfo(CheckProjectNO){
            var params={
                CheckProjectNO:CheckProjectNO
            }
            this.axios.get('/lims/Sample',{params:params}).then((res) => {
                this.Discerns=res.data.data[0].Discern
                this.Inspects=res.data.data[0].Inspect
                this.Characters=res.data.data[0].Character
                this.Contents=res.data.data[0].Content
                this.Characters=res.data.data[0].Character
                this.Microbes=res.data.data[0].Microbe
            })
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.SearchTab()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.SearchTab()
        },
    },
}
</script>
<style scoped>

</style>