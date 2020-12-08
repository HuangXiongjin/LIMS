<template>
    <el-row :gutter="20">
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
                        <el-button type="danger">重置</el-button>
                        <el-button type="success" @click="postRequest">提交</el-button>
                        <el-button type="info">加急申请</el-button>
                       </div>
                   </el-col>
                </div>
            </el-col>
        </el-col>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){

        return {
           msg:'12',
           requestform:{Specs:'',CheckNumber:'',Name:'',ProductNumber:'',Supplier:'',Number:'',Amount:'',Unit:''},
           projectform:{CheckProcedure:'',CheckDepartment:'',CheckDate:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),CheckUser:localStorage.getItem('Name'),Comment:''},
           treeDom:[],
           defaultProps: {
            children: 'children',
            label: 'label'
            },
            currentgoods:'物料类'
        }
    },
    created(){
        this.getInitTree()
    },
    methods: {
        getInitTree() { //获取初始树形结构
            this.axios.get('/lims/Tree').then((res) => {
                if(res.data.code==='1000'){
                    this.treeDom=res.data.data
                }
            })
        },
        showTabInfo(obj,data,node){
            this.currentgoods=obj.label
            
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
                CheckProcedure:this.projectform.CheckProcedure,
                CheckDepartment:this.projectform.CheckDepartment,
                CheckDate:moment(this.projectform.CheckDate).format('YYYY-MM-DD HH:mm:ss'),
                CheckUser:this.projectform.CheckUser,
                Comment:this.projectform.Comment,
            }
            this.axios.post('https://yapi.baidu.com/mock/10425/CheckForm',this.qs.stringify(params)).then(res=>{
                if(res.data.code=='1000'){
                    this.$message({
                        type:'success',
                        message:'提交成功'
                    })
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
</style>