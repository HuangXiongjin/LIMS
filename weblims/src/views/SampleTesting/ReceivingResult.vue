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
                        <el-col :span='6' class="req mgl15" style="paddingTop:3px;">
                             <el-radio-group v-model="radio2" @change="HandSelectChange">
                                <el-radio-button label="样本分发" ></el-radio-button>
                                <el-radio-button label="记录分发"></el-radio-button>
                             </el-radio-group>
                        </el-col>
                    </el-row>
                </el-col>
                <el-col :span='24'>
                      <el-row class="padd15" v-if="radio2=='样本分发'">
                          <el-col :span='24' class="container mgt24" style="backgroundColor:#EAEAEA;">
                              <el-col :span='24'>
                                  <el-col :span='24' class="lightgreen fsz20"><el-checkbox label="去检验" checked></el-checkbox></el-col>
                                  <el-col :span='24' class="mgt24">
                                      <el-row :gutter='10'>
                                          <el-col :span='4'>样品品名</el-col>
                                          <el-col :span='3'>类别</el-col>
                                          <el-col :span='4'>批号(物料代码)</el-col>
                                          <el-col :span='3'>分配样量</el-col>
                                          <el-col :span='3'>编号</el-col>
                                          <el-col :span='7'>分配小组</el-col>
                                      </el-row>
                                  </el-col>
                                  <el-col :span='24' class="mgt24">
                                       <el-row>
                                          <el-col :span='4' class="lightgreen padt8">{{Row.Product}}</el-col>
                                          <el-col :span='3' class="lightgreen padt8">{{Row.ProductType}}</el-col>
                                          <el-col :span='4' class="lightgreen padt8">{{Row.Number}}</el-col>
                                          <el-col :span='3' class="lightgreen padt8">{{Record.JNumber}}</el-col>
                                          <el-col :span='3' class="lightgreen padt8">{{Record.No}}</el-col>
                                          <el-col :span='7'>
                                              <el-select v-model="RecordForm.group" multiple placeholder="请选择" style="width:100%;">
                                                <el-option
                                                v-for="item in Groups"
                                                :key="item.value"
                                                :label="item.label"
                                                :value="item.label">
                                                </el-option>
                                            </el-select>
                                          </el-col>
                                      </el-row>
                                  </el-col>
                              </el-col>
                              <el-col :span='24'>
                                  <el-col class="padtop50 padl40" style="textAlign:right;"><el-button type="success" @click="DistributeSample" v-if="IsDoing" :disabled="curSta=='已分发'">{{curSta}}</el-button></el-col>
                              </el-col>
                          </el-col>
                      </el-row>
                </el-col>
            </el-row>
            <el-row v-if="radio2=='记录分发'" class="mgt24">
                 <el-col :span='24' class="container">
                    <el-menu :default-active="'1'" class="bgwhite mgt24" mode="horizontal" @select="handleSelect">
                        <el-menu-item :index="'1'" style="height:46px;lineHeight:30px;" v-if="Discernopt">检验记录</el-menu-item>
                    </el-menu>
                    <div>
                        <div class="mgt24 mgb24">产品检验原始记录</div>
                        <div style="border:1px solid #ccc;paddingTop:26px;">
                            <el-form ref="form" :model="RecordForm" label-width="100px">
                                <el-row>
                                    <el-col :span='11'>
                                        <el-form-item label="品名：">
                                            <el-input v-model="Row.Product" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="批号：">
                                            <el-input v-model="Row.ProductNumber" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="规格：">
                                            <el-input v-model="Row.Specs" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="请验部门：">
                                            <el-input v-model="Row.CheckDepartment" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="剂型：">
                                            <el-input v-model="Recordobj.Type" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="批数量：">
                                            <el-input v-model="Row.Amount" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='11'>
                                        <el-form-item label="取样时间：">
                                            <el-input v-model="batchinfo[2].CheckDate" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span='11'>
                                        <el-form-item label="检验日期：">
                                            <el-input v-model="Recordobj.CheckTime" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                                <el-row >
                                    <el-col :span='22'>
                                        <el-form-item label="检验依据：">
                                            <el-input v-model="Recordobj.Basis" :disabled="true"></el-input>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                            </el-form>
                            <el-col class="mgt24">
                            <el-form >
                                <el-col :span='22'>
                                    <el-tag type="info">【鉴别】：</el-tag>
                                    <p v-for="(item,index) in Discerns" :key='index' class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="success">【检查】：</el-tag>
                                    <p v-for="(item,index) in Inspects" :key='index' class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="warning">【性状】：</el-tag>
                                    <p v-for="(item,index) in Characters" :key='index' class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="danger">【含量测定】：</el-tag>
                                    <p v-for="(item,index) in Contents" :key='index'  class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="info">【微生物限度】：</el-tag>
                                    <p v-for="(item,index) in Microbes" :key='index'  class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                </el-col>
                            </el-form>
                            </el-col>
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
           batchinfo:[{Status:'申请'},{Status:'请验审核'},{Status:'取样'},{Status:'接收'},{Status:'分发'},{Status:'质检'},{Status:'报告'},{Status:'质检审核'},{Status:'放行'}],
           IsDoing:JSON.parse(sessionStorage.getItem('Rights').replace(/'/g, '"')).includes("样本及记录分发"),
           currentstep:4,
           curSta:'确认分发',
           Discernopt:true,
           Checkopt:false,
           Lyopt:false,
           RecordForm:{
               group:[]
           },
           opstate: [{value: '申请',label: '申请'},{value: '请验审核',label: '请验审核'}, {value: '取样',label: '取样'},{value: '接收',label: '接收'},{value: '分发',label: '分发'},
            {value: '质检',label: '质检'},{value: '报告',label: '报告'}, {value: '质检审核',label: '质检审核'},{value: '放行',label: '放行'}],
           Groups:[{label:"产品组",value:1},{label:"物料组",value:2},{label:"微生物组",value:3}],
           LyForm:{
               PackSpecs:'',
               TheoreticalYield:'',
               BatchAmount:'',
               BatchDepartment:'',
               BatchName:'',
               Position:'',
               BatchTime:'',
               Handler:'',
               ProductionDate:'',
               ValidityDate:'',
               Comment:''
           },
           Row:{},
           distribute:{
               no1:'',
               Account1:'',
               no2:'',
               Account2:'',
               no3:'',
               Account3:'',
               CheckProjectNO:'',

           },
           currentChoose:'2',
           radio2:'样本分发',
           Recordobj:{
               Basis:'',
               Type:'',
               CheckTime:''
           },
           Record:{},
           searchObj:{
               category:'玉米淀粉',
               state:'分发',
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
            Discerns:[],
            Inspects:[],
            Characters:[],
            Contents:[],
            Microbes:[],
            batchtableconfig:[{prop:'CheckNumber',label:'请验单号'},{prop:'Product',label:'品名'},{prop:'CheckDate',label:'请验时间',width:155}],//批次列表
        }
    },
    created(){
       this.getSelectOption()
       this.SearchTab()
    },
    methods: {
        getCurrentSteps(CheckProjectNO){ //获取进度条
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
        HandSelectChange(e){
            this.radio2=e
        },
       getRecord(){
           var params={
               TableName:"Distribute",
               Query:"Accurate", 
               QueryColumnName:"CheckProjectNO",
               QueryColumnValue:this.distribute.CheckProjectNO,
               QueryColumnName2:"Status",
               QueryColumnValue2:"J"
           }
           this.axios.get('/lims/CRUD',{params:params}).then((res) => {
               if(res.data.code=='1000' && res.data.data!=null){
                   this.Record=res.data.data[0]
               }
           })
       },
        DistributeSample(){ //检验接收记录
            var params={
                 Group:JSON.stringify(this.RecordForm.group),
                 CheckProjectNO:this.distribute.CheckProjectNO,
                 GroupUser:localStorage.getItem('Name'),
                 Action:JSON.stringify(['Q']),
                 Time:moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
            }
           this.axios.post('/lims/Distribute',this.qs.stringify(params)).then((res) => {
               if(res.data.code=='1000'){
                   this.$message({
                       type:'success',
                       message:'分发成功'
                   })
                   this.curSta='已分发'
               }else{
                   this.$message({
                       type:'info',
                       message:'请重试'
                   })
               }
           })
        },
        handleSelect(key) { //区分样品和记录
            this.currentChoose=key
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
                }
            })
        },
        handletabClick(row){ //左侧tab点击事件
            this.curSta='确认分发'
            this.Row=row
            this.RecordForm.CheckTime=moment(new Date()).format('YYYY-MM-DD HH:mm:ss')
            this.distribute.CheckProjectNO=row.CheckProjectNO
            this.getJbInfo(row.CheckProjectNO)
            this.getCurrentSteps(row.CheckProjectNO)
            this.getRecord()
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
     .jbcontent{
         height:30px;
         line-height:30px;
     }
</style>
