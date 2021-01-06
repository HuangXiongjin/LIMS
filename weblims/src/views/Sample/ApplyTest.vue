<template>
    <el-row :gutter="20">
        <el-col :span='24' class="mgt24 mgb24 container">
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
        <el-col :span='5'>
            <el-col class="container">
                <div class="fontWet titl">样本分类</div>
                <div style="marginTop:20px;">
                    <el-tree
                    :data="treeDom"
                    node-key="id"
                    default-expand-all
                    :expand-on-click-node="false"
                    :props="defaultProps"
                    highlight-current
                    @node-click='showTabInfo'>
                    </el-tree>
                </div>
            </el-col>
        </el-col>
        <el-col :span='19'>
            <el-col class="container">
                <div class="fontWet titl">请验单填写</div>
                <div style="marginTop:20px;" class="padd15">
                   <el-col :span='24' class="txtgreencolor fsz20">{{currentgoods}}</el-col>
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
                            <el-form-item label="请验部门">
                                <el-input v-model="projectform.CheckDepartment"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="请验工序">
                                <el-input v-model="projectform.CheckProcedure"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="物料类别">
                                <el-input v-model="projectform.ProductType"></el-input>
                            </el-form-item>
                           </el-col>
                           <el-col :span='10'>
                            <el-form-item label="备注">
                                <el-input type="textarea" v-model="projectform.Comment"></el-input>
                            </el-form-item>
                           </el-col>
                            <el-col :span='10'>
                            <el-form-item label="请验项目" class="PuNo">
                                <el-button type='primary' @click="selectJbChoice">点击选择请验项目</el-button>
                            </el-form-item>
                           </el-col>
                         </el-row>
                       </el-form>
                   </el-col>
                   <el-col :span='24' class="padd15">
                       <el-collapse v-model="activeNames">
                            <el-collapse-item title="性状" name="Character">
                                <div v-for="(item,index) in projectform.CheckProject['Character']" :key='index' class="lightgreen">{{item}}</div>
                            </el-collapse-item>
                            <el-collapse-item title="鉴别" name="Discern">
                                <div v-for="(item,index) in projectform.CheckProject['Discern']" :key='index' class="lightgreen">{{item}}</div>
                            </el-collapse-item>
                            <el-collapse-item title="检查" name="Inspect">
                                <div v-for="(item,index) in projectform.CheckProject['Inspect']" :key='index' class="lightgreen">{{item}}</div>
                            </el-collapse-item>
                            <el-collapse-item title="含量测定" name="Content">
                                <div v-for="(item,index) in projectform.CheckProject['Content']" :key='index' class="lightgreen">{{item}}</div>
                            </el-collapse-item>
                            <el-collapse-item title="微生物限度" name="Microbe">
                                <div v-for="(item,index) in projectform.CheckProject['Microbe']" :key='index' class="lightgreen">{{item}}</div>
                            </el-collapse-item>
                        </el-collapse>
                   </el-col>
                   <el-col :span='24'>
                       <div style="float:right;">
                        <el-button type="danger" @click="ResetRequest">重置</el-button>
                        <el-button type="success" @click="postRequest">提交</el-button>
                        <el-button type="info">加急申请</el-button>
                       </div>
                   </el-col>
                </div>
            </el-col>
        </el-col>
        <el-dialog title="检验项选择" :visible.sync="jbTableVisible">
            <el-form :model="projectform" class="jbform" style="overflow:hidden;">
                <el-form-item label='鉴别' class="mgb10">
                     <el-select v-model="projectform.CheckProject['Discern']" multiple placeholder="请选择">
                          <el-option v-for="(item,index) in jbarr" :key="index" :label="item.value" :value="item.value"></el-option>
                     </el-select>
                </el-form-item>
                <el-form-item label='性状' class="mgb10">
                     <el-select v-model="projectform.CheckProject['Character']" multiple placeholder="请选择">
                          <el-option v-for="(item,index) in xzarr" :key="index" :label="item.value" :value="item.value"></el-option>
                     </el-select>
                </el-form-item>
                <el-form-item label='检查' class="mgb10">
                     <el-select v-model="projectform.CheckProject['Inspect']" multiple placeholder="请选择">
                          <el-option v-for="(item,index) in jcarr" :key="index" :label="item.value" :value="item.value"></el-option>
                     </el-select>
                </el-form-item>
                <el-form-item label='含量测定' class="mgb10">
                     <el-select v-model="projectform.CheckProject['Content']" multiple placeholder="请选择">
                          <el-option v-for="(item,index) in hlcdarr" :key="index" :label="item.value" :value="item.value"></el-option>
                     </el-select>
                </el-form-item>
                <el-form-item label='微生物限度' class="mgb10">
                     <el-select v-model="projectform.CheckProject['Microbe']" multiple placeholder="请选择">
                          <el-option v-for="(item,index) in wswarr" :key="index" :label="item.value" :value="item.value"></el-option>
                     </el-select>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="jbTableVisible = false">取 消</el-button>
                <el-button type="primary" @click="jbTableVisible = false">确 定</el-button>
            </div>
        </el-dialog>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){

        return {
           currentstep:0,
           checkNo:'',
           batchinfo:[{Status:'申请'},{Status:'请验审核'},{Status:'取样'},{Status:'接收'},{Status:'分发'},{Status:'质检'},{Status:'报告'},{Status:'质检审核'},{Status:'放行'}],
           activeNames:['Discern','Character','Inspect','Content','Microbe'],
           requestform:{Specs:'',CheckNumber:'',Name:'',ProductNumber:'',Supplier:'',Number:'',Amount:'',Unit:''},
           projectform:{
               CheckProcedure:'',CheckDepartment:'',ProductType:'',
               CheckProject:{Discern:[],Character:[],Inspect:[],Content:[],Microbe:[]}
           },
           treeDom:[],
           defaultProps: {
            children: 'children',
            label: 'label'
            },
            currentgoods:'物料类',
            jbarr:[],
            jcarr:[],
            xzarr:[],
            hlcdarr:[],
            wswarr:[],
            jbTableVisible:false
        }
    },
    created(){
        this.getInitTree()
    },
    methods: {
        getCurrentSteps(){
           var params={
                Action:'p',
                CheckProjectNO:this.checkNo
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
        ResetRequest(){
            this.requestform={Specs:'',CheckNumber:'',Name:'',ProductNumber:'',Supplier:'',Number:'',Amount:'',Unit:''}
            this.projectform={
               CheckProcedure:'',CheckDepartment:'',
               Comment:'',
               ProductType:'',
               CheckProject:{Discern:[],Character:[],Inspect:[],Content:[],Microbe:[]}
           }
        },
        selectJbChoice(){
            this.jbTableVisible=true
        },
        getJB(Id){
             var params={
                No:Id
            }
            this.axios.get('/lims/QualityStandard',{params:params}).then((res) => {
                this.jbarr=res.data.data[0]['Discern']
                this.jcarr=res.data.data[0]['Inspect']
                this.xzarr=res.data.data[0]['Character']
                this.hlcdarr=res.data.data[0]['Content']
                this.wswarr=res.data.data[0]['Microbe']
            })
        },
        getInitTree() { //获取初始树形结构
            this.axios.get('/lims/Tree').then((res) => {
                if(res.data.code==='1000'){
                    this.treeDom=res.data.data
                }
            })
        },
        showTabInfo(obj,data,node){
            this.projectform.ProductType=data.parent.data.label
            this.currentgoods=obj.label
            this.requestform.Name=obj.label
            this.getJB(obj.id)
        },
        postRequest(){
            var params={
                CheckNumber:this.requestform.CheckNumber,
                Name:this.requestform.Name,
                Specs:this.requestform.Specs,
                Supplier:this.requestform.Supplier,
                ProductNumber:this.requestform.ProductNumber,
                Number:this.requestform.Number,
                Amount:this.requestform.Amount,
                Unit:this.requestform.Unit,
                ProductType:this.projectform.ProductType,
                CheckProcedure:this.projectform.CheckProcedure,
                CheckDepartment:this.projectform.CheckDepartment,
                CheckDate:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
                CheckUser:localStorage.getItem('Name'),
                Comment:this.projectform.Comment,
                CheckProject:JSON.stringify(this.projectform.CheckProject),
            }
            this.axios.post('/lims/CheckForm',this.qs.stringify(params)).then(res=>{
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'提交成功'
                    })
                    this.checkNo=res.data.data
                    this.getCurrentSteps()
                }
            })
        }
    },
}
</script>
<style scoped>
    .titl{
        height:46px;
        line-height:46px;
        border-bottom:1px solid #ccc;
    }
    .jbform .el-select{
        width: 100%;
    }
</style>