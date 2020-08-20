<template>
    <el-row>
        <el-col :span='24'>
            <el-steps :active="steps" finish-status="wait" align-center class="marginBottom">
                <el-step @click.native="clickStep(0)" class="cursor-pointer" title="批次号品名录入"></el-step>
                <el-step @click.native="clickStep(1)" class="cursor-pointer" title="批次计划"></el-step>
                <el-step @click.native="clickStep(2)" class="cursor-pointer" title="计划效验结果"></el-step>
            </el-steps>
        </el-col>
        <el-col :span='24' class="platformContainer" v-if='steps===0'>
            <div class="text-size-18 marginBottom">计划实际信息</div>
            <el-form :model="formInline" class="demo-form-inline">
                <el-form-item>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">制定计划日期</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">制定计划日期</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">品名</el-col>
                    <el-col :span='6'>
                        <el-select v-model="formInline.region" placeholder="请选择品名">
                            <el-option label="区域一" value="shanghai"></el-option>
                            <el-option label="区域二" value="beijing"></el-option>
                        </el-select>
                    </el-col>
                </el-form-item>
                <el-form-item>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">计划重量</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">生产线</el-col>
                    <el-col :span='6'>
                        <el-input v-model="formInline.user"></el-input>
                    </el-col>
                    <el-col :span='2' style="textAlign:right;paddingRight:8px;">单位</el-col>
                    <el-col :span='6'>
                        <el-select v-model="formInline.region" placeholder="请选择单位">
                            <el-option label="kg" value="shanghai"></el-option>
                            <el-option label="h" value="beijing"></el-option>
                        </el-select>
                    </el-col>
                </el-form-item>
            </el-form>
        </el-col>
        <el-col>
            <div class="platformContainer" v-if='steps===0'>
                <tableView class="" :tableData="PermissionTableData1" @getTableData="getPermissionTable"></tableView>
            </div>
        </el-col>
        <el-col>
            <div class="platformContainer" v-if='steps===1'>
                <div class="marginBottom text-size-18">生成计划信息</div>
                <tableView class="" :tableData="PermissionTableData2" @getTableData="getPermissionTable"></tableView>
            </div>
        </el-col>
        <el-col v-if="steps===2">
            <div class="platformContainer" style="textAlign:center;height:200px;fontSize:20px;lineHeight:200px;">
              计划检验结果：新增计划成功
            </div>
        </el-col>
    </el-row>
</template>
<script>
 import tableView from '@/components/CommonTable'
export default {
    components:{tableView},
    data() {
        return {
            steps:0,
            formInline: {
                user: '',
                region: ''
            },
           PermissionTableData1:{
            tableName:"Scheduling",
            column:[
                {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
                {prop:"PRName",label:"产品名称",type:"input",value:""},
                {prop:"SchedulingTime",label:"排产时间(工厂日历)",type:"input",value:""},
                {prop:"SchedulingNum",label:"排产序列号",type:"input",value:""},
                {prop:"BatchNumS",label:"批数",type:"input",value:""},
                {prop:"SchedulingStatus",label:" 排产状态",type:"input",value:""},
                {prop:"create_time",label:" 创建时间",type:"input",value:"",canSubmit:false,searchProp:false},
                {prop:"update_time ",label:" 修改时间",type:"input",value:"",canSubmit:false,searchProp:false},
            ],
            data:[],
            limit:5,
            offset:1,
            total:0,
            tableSelection:true, //是否在第一列添加复选框
            searchProp:"",
            searchVal:"",
            multipleSelection: [],
        },
        PermissionTableData2:{
            tableName:"PlanManager",
            column:[
                {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
                {prop:"SchedulePlanCode",label:"调度编号",type:"input",value:""},
                {prop:"BatchID",label:"批次号",type:"input",value:""},
                {prop:"PlanQuantity",label:"计划重量",type:"input",value:""},
                {prop:"Unit",label:"单位",type:"input",value:""},
                {prop:"BrandCode",label:" 品名编码",type:"input",value:""},
                {prop:"BrandName",label:" 品名",type:"input",value:"",canSubmit:false,searchProp:false},
                {prop:"PlanStatus ",label:"计划状态",type:"input",value:"",canSubmit:false,searchProp:false},
                {prop:"PlanBeginTime ",label:"调度计划开始时间",type:"input",value:"",canSubmit:false,searchProp:false},
                {prop:"PlanEndTime ",label:" 计划完成时间",type:"input",value:"",canSubmit:false,searchProp:false},
                {prop:"Type ",label:"调度类型",type:"input",value:"",canSubmit:false,searchProp:false},
            ],
            data:[],
            limit:5,
            offset:1,
            total:0,
            tableSelection:true, //是否在第一列添加复选框
            searchProp:"",
            searchVal:"",
            multipleSelection: [],
        }
        }
    },
    created(){
      this.getPermissionTable()
    },
    methods:{
      getPermissionTable(){
        var that = this
        var params = {
          tableName: this.PermissionTableData1.tableName,
          limit:this.PermissionTableData1.limit,
          offset:this.PermissionTableData1.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.PermissionTableData1.data = data.rows
            that.PermissionTableData1.total = data.total
          }
        },res =>{
          console.log("请求错误")
        }
        )
      },
      clickStep(index){
        this.steps = index
      }
    }
}
</script>
<style scoped>
  .productionstep .el-steps--simple{
      background-color:#ddd;
  }
</style>
