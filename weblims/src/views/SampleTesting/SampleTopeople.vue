<template>
    <el-row :gutter='20'>
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
                             <el-radio-group v-model="radio2" @change='handSelectChange'>
                                <el-radio-button label="样本分发" ></el-radio-button>
                                <el-radio-button label="记录分发"></el-radio-button>
                             </el-radio-group>
                        </el-col>
                    </el-row>
                </el-col>
            </el-row>
            <el-row v-if="radio2=='样本分发'" class="mgt24">
                <div  class="padd15 container" style="height:700px;overflow:auto;">
                    <el-col :span='24'>
                      <el-row>
                          <div class="mgt24 lightgreen">详细信息</div>
                          <el-col :span='24' class="mgt24">
                              <el-form :inline="true">
                                <el-col :span='8'>
                                  <el-form-item label="品名">
                                    <el-input v-model="Row.Name" placeholder="品名"></el-input>
                                  </el-form-item>
                               </el-col>
                               <el-col :span='8'>
                                 <el-form-item label="类别">
                                    <el-input v-model="Row.ProductType" placeholder="类别"></el-input>
                                </el-form-item>
                               </el-col>
                               <el-col :span='8'>
                                 <el-form-item label="分配样量">
                                    <el-input v-model="Row.JAccount" placeholder="分配样量"></el-input>
                                </el-form-item>
                               </el-col>
                               <el-col :span='8'>
                                 <el-form-item label="批号">
                                    <el-input v-model="Row.ProductNumber" placeholder="批号"></el-input>
                                </el-form-item>
                               </el-col>
                               <el-col :span='8'>
                                 <el-form-item label="编号">
                                    <el-input v-model="Row.Foo" placeholder="编号"></el-input>
                                </el-form-item>
                               </el-col>
                              </el-form>
                          </el-col>
                      </el-row>
                      <el-row :gutter='24'>
                              <div class="lightgreen padd15">分配操作</div>
                              <el-row class="padd15">
                               <el-col :span='12'>
                                  <el-select v-model="distribute.worker" placeholder="请选择人">
                                    <el-option
                                    v-for="item in workers"
                                    :key="item.ID"
                                    :label="item.Name"
                                    :value="item.Name">
                                    </el-option>
                                </el-select>
                               </el-col>
                               <el-col :span='12'>
                                  <el-select v-model="distribute.Discern" multiple collapse-tags placeholder="选择鉴别">
                                    <el-option
                                    v-for="item in jbarr.Discern"
                                    :key="item.label"
                                    :label="item.value"
                                    :value="item.value">
                                    </el-option>
                                </el-select>
                               </el-col>
                              </el-row>
                              <el-row class="padd15">
                               <el-col :span='12'>
                                  <el-select v-model="distribute.Inspect" multiple collapse-tags placeholder="选择检查">
                                    <el-option
                                    v-for="item in jbarr.Inspect"
                                    :key="item.label"
                                    :label="item.value"
                                    :value="item.value">
                                    </el-option>
                                </el-select>
                               </el-col>
                               <el-col :span='12'>
                                  <el-select v-model="distribute.Microbe" multiple collapse-tags placeholder="选择微生物">
                                    <el-option
                                    v-for="item in jbarr.Microbe"
                                    :key="item.label"
                                    :label="item.value"
                                    :value="item.value">
                                    </el-option>
                                </el-select>
                              </el-col>
                            </el-row>
                            <el-row class="padd15">
                               <el-col :span='12'>
                                  <el-select v-model="distribute.Content" multiple collapse-tags placeholder="选择含量">
                                    <el-option
                                    v-for="item in jbarr.Content"
                                    :key="item.label"
                                    :label="item.value"
                                    :value="item.value">
                                    </el-option>
                                </el-select>
                               </el-col>
                               <el-col :span='12'>
                                  <el-select v-model="distribute.Character" multiple collapse-tags placeholder="选择性状">
                                    <el-option
                                    v-for="item in jbarr.Character"
                                    :key="item.label"
                                    :label="item.value"
                                    :value="item.value">
                                    </el-option>
                                </el-select>
                               </el-col>
                              </el-row>
                              <el-row class="padd15">
                                <el-col :span='24' style="textAlign:right;"><el-button type="success" @click="distributeToPeople" v-if="IsDoing">确定分发</el-button></el-col>
                              </el-row>
                              <div>
                              <el-col :span='22'>
                                    <el-tag type="info">【鉴别】：</el-tag>
                                    <p v-for="(item,index) in distribute.Discern" :key='index' class="lightgreen jbcontent fsz10">{{item}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="success">【检查】：</el-tag>
                                    <p v-for="(item,index) in distribute.Inspect" :key='index' class="lightgreen jbcontent fsz10">{{item}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="warning">【性状】：</el-tag>
                                    <p v-for="(item,index) in distribute.Character" :key='index' class="lightgreen jbcontent fsz10">{{item}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="danger">【含量测定】：</el-tag>
                                    <p v-for="(item,index) in distribute.Content" :key='index'  class="lightgreen jbcontent fsz10">{{item}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="info">【微生物限度】：</el-tag>
                                    <p v-for="(item,index) in distribute.Microbe" :key='index'  class="lightgreen jbcontent fsz10">{{item}}</p>
                                </el-col>
                            </div>
                          </el-row>
                </el-col>
                </div>
            </el-row>
            <el-row v-if="radio2=='记录分发'" class="mgt24">
                 <el-col :span='24' class="container">
                    <el-menu :default-active="'1'" class="bgwhite mgt24" mode="horizontal">
                        <el-menu-item :index="'1'" style="height:46px;lineHeight:30px;">检验记录</el-menu-item>
                    </el-menu>
                    <div>
                        <div class="mgt24 mgb24">产品检验原始记录</div>
                        <div style="border:1px solid #ccc;paddingTop:26px;">
                            <el-form ref="form" label-width="100px">
                                <el-row>
                                    <el-col :span='11' class="mgt14">
                                        <el-form-item label="品名：">
                                            <el-input v-model="Row.Name" :disabled="true"></el-input>
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
                                            <el-input v-model="Row.VerifyDate" :disabled="true"></el-input>
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
                                <el-col :span='22'>
                                    <el-tag type="info">【鉴别】：</el-tag>
                                    <p v-for="(item,index) in jbarr.Discern" :key='index' class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="success">【检查】：</el-tag>
                                    <p v-for="(item,index) in jbarr.Inspect" :key='index' class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="warning">【性状】：</el-tag>
                                    <p v-for="(item,index) in jbarr.Character" :key='index' class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="danger">【含量测定】：</el-tag>
                                    <p v-for="(item,index) in jbarr.Content" :key='index'  class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                    <el-divider></el-divider>
                                </el-col>
                                <el-col :span='22'>
                                    <el-tag type="info">【微生物限度】：</el-tag>
                                    <p v-for="(item,index) in jbarr.Microbe" :key='index'  class="lightgreen jbcontent fsz10">{{item.value}}</p>
                                </el-col>
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
           IsDoing:sessionStorage.getItem('Rights').replace(/'/g, '"').includes("样本及记录分发"),
           currentstep:4,
           batchinfo:[{Status:'申请'},{Status:'请验审核'},{Status:'取样'},{Status:'接收'},{Status:'分发'},{Status:'质检'},{Status:'报告'},{Status:'质检审核'},{Status:'放行'}],
           opstate: [{value: '申请',label: '申请'},{value: '请验审核',label: '请验审核'}, {value: '取样',label: '取样'},{value: '接收',label: '接收'},{value: '分发',label: '分发'},
            {value: '质检',label: '质检'},{value: '报告',label: '报告'}, {value: '质检审核',label: '质检审核'},{value: '放行',label: '放行'}
            ],
           showstep:false,
           workers:[],
           Row:{},
           distribute:{ //选择绑定的集合
               CheckProjectNO:'',
               worker:'',
               Discern:[],
               Inspect:[],
               Microbe:[],
               Content:[],
               Character:[],
           },
           radio2:'样本分发',
           Recordobj:{},
           jbarr:{ //获取到集合
               Discern:[],
               Inspect:[],
               Microbe:[],
               Content:[],
               Character:[],
           },
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
            batchtableconfig:[{prop:'CheckNumber',label:'请验单号'},{prop:'Name',label:'品名'},{prop:'CheckDate',label:'请验时间',width:155}],//批次列表
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
        distributeToPeople(){
            var params={
                CheckProjectNO:this.distribute.CheckProjectNO,
                Worker:this.distribute.worker,
                Discern:JSON.stringify(this.distribute.Discern),
                Inspect:JSON.stringify(this.distribute.Inspect),
                Microbe:JSON.stringify(this.distribute.Microbe),
                Content:JSON.stringify(this.distribute.Content),
                Character:JSON.stringify(this.distribute.Character),
                CheckStartTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
                Name:localStorage.getItem('Name')
            }
            this.axios.post('/lims/Worker',this.qs.stringify(params)).then((res) => {
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'下发操作成功'
                    })
                }else{
                   this.$message({
                        type:'error',
                        message:'下发操作失败，请重试'
                    }) 
                }
            })
        },
       getWorker(){ //获取分组和人员
           var params={
               CheckProjectNO:this.distribute.CheckProjectNO,
               Name:localStorage.getItem('Name')
           }
           this.axios.get('/lims/Worker',{params:params}).then((res) => {
               if(res.data.code=='1000'){
                   this.workers=res.data.data
               }else{
                   this.$message({
                       type:'warning',
                       message:'无权限，获取小组人员失败'
                   })
               }
           })
       },
       getRecord(){ //获取记录项数据
           var params={
               CheckProjectNO:this.distribute.CheckProjectNO
           }
           this.axios.get('/lims/CheckRecord',{params:params}).then((res) => {
               if(res.data.code=='1000' && res.data.data!=null){
                   this.Recordobj=res.data.data
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
        handSelectChange(e){
            this.radio2=e
        },
        handletabClick(row){ //左侧tab点击事件
            this.Row=row
            this.distribute.CheckProjectNO=row.CheckProjectNO
            this.getJbInfo(row.CheckProjectNO)
            this.getRecord()
            this.getWorker()
            this.getCurrentSteps(row.CheckProjectNO)
        },
        getJbInfo(CheckProjectNO){
            var params={
                CheckProjectNO:CheckProjectNO
            }
            this.axios.get('/lims/Sample',{params:params}).then((res) => {
                this.jbarr.Discern=res.data.data[0].Discern.map((item, index) => {
                    return {label:item.ID,value:item.value}
                })
                this.jbarr.Inspect=res.data.data[0].Inspect.map((item, index) => {
                    return {label:item.ID,value:item.value}
                })
                this.jbarr.Character=res.data.data[0].Character.map((item, index) => {
                    return {label:item.ID,value:item.value}
                })
                this.jbarr.Content=res.data.data[0].Content.map((item, index) => {
                    return {label:item.ID,value:item.value}
                })
                this.jbarr.Microbe=res.data.data[0].Microbe.map((item, index) => {
                    return {label:item.ID,value:item.value}
                })
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
