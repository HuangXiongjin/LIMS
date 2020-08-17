<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">工艺段生产计划</span>
      </div>
      <div class="platformContainer">
        <tableView class="" :tableData="PermissionTableData" @getTableData="getPermissionTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    components:{tableView},
    data(){
      return {
        PermissionTableData:{
          tableName:"ZYPlan",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"PlanDate",label:"计划日期",type:"input",value:""},
            {prop:"PlanNo",label:"制药计划单号",type:"input",value:""},
            {prop:"BatchID",label:"批次号",type:"input",value:""},
            {prop:"PlanSeq",label:" 顺序号",type:"input",value:""},
            {prop:"PUID",label:"工艺段",type:"input",value:""},
            {prop:"PlanType",label:" 计划类型",type:"input",value:""},
            {prop:"BrandID",label:"品名",type:"input",value:""},
            {prop:"BrandName",label:"品名名称",type:"input",value:""},
            {prop:"ERPOrderNo",label:"ERP订单号",type:"input",value:""},
            {prop:"PlanQuantity",label:"计划重量",type:"input",value:""},
            {prop:"ActQuantity",label:"实际重量",type:"input",value:""},
            {prop:"Unit",label:"单位",type:"input",value:""},
            {prop:"EnterTime",label:"录入时间",type:"input",value:""},
            {prop:"PlanBeginTime",label:"计划开始时间",type:"input",value:""},
            {prop:"PlanEndTime",label:"计划结束时间",type:"input",value:""},
            {prop:"ActBeginTime",label:"实际开始时间",type:"input",value:""},
            {prop:"ActEndTime",label:"实际结束时间",type:"input",value:""},
            {prop:"ZYPlanStatus",label:"计划状态",type:"input",value:""},
            {prop:"LockStatus",label:"计划锁定状态",type:"input",value:""},
          ],
          data:[],
          limit:5,
          offset:1,
          total:0,
          tableSelection:true, //是否在第一列添加复选框
          searchProp:"",
          searchVal:"",
          multipleSelection: [],
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            {type:"primary",label:"添加"},
            {type:"warning",label:"修改"},
            {type:"danger",label:"删除"},
          ],
        },
      }
    },
    created(){
      this.getPermissionTable()
    },
    methods:{
      getPermissionTable(){
        var that = this
        var params = {
          tableName: this.PermissionTableData.tableName,
          limit:this.PermissionTableData.limit,
          offset:this.PermissionTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.PermissionTableData.data = data.rows
            that.PermissionTableData.total = data.total
          }
        },res =>{
          console.log("请求错误")
        }
        )
      },
    }
  }
</script>

<style scoped>

</style>
