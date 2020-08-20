<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">生产调度信息</span>
      </div>
      <div class="platformContainer">
        <tableView class="" :tableData="PlanTableData" @getTableData="getPlanTable"></tableView>
      </div>
      <div class="platformContainer">
        <tableView class="" :tableData="ProcessPlanTableData" @getTableData="getProcessPlanTable"></tableView>
      </div>
      <div class="platformContainer">
        <tableView class="" :tableData="ProcessTaskTableData" @getTableData="getProcessTaskTable"></tableView>
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
        PlanTableData:{
          tableName:"PlanManager",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"SchedulePlanCode",label:"调度编号",type:"input",value:""},
            {prop:"BatchID",label:" 批次号",type:"input",value:""},
            {prop:"PlanQuantity",label:"计划重量",type:"input",value:""},
            {prop:"Unit",label:"单位",type:"input",value:""},
            {prop:"BrandCode",label:"品名ID",type:"input",value:""},
            {prop:"BrandName",label:"品名",type:"input",value:""},
            {prop:"PlanStatus",label:"计划状态",type:"input",value:""},
            {prop:"PlanBeginTime",label:"调度计划开始时间",type:"input",value:""},
            {prop:"PlanEndTime",label:"计划完成时间",type:"input",value:""},
            {prop:"Type",label:"调度类型",type:"input",value:""}
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
        ProcessPlanTableData:{
          tableName:"ZYPlan",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"PlanDate",label:"计划日期",type:"input",value:""},
            {prop:"PlanNo",label:"制药计划单号",type:"input",value:""},
            {prop:"BatchID",label:"批次号",type:"input",value:""},
            {prop:"PlanSeq",label:" 顺序号",type:"input",value:""},
            {prop:"PUCode",label:"工艺段编码",type:"input",value:""},
            {prop:"PlanType",label:" 计划类型",type:"input",value:""},
            {prop:"BrandCode",label:"品名",type:"input",value:""},
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
        ProcessTaskTableData:{
          tableName:"ZYTask",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"EquipmentID",label:"设备ID",type:"input",value:""},
            {prop:"PlanDate",label:"计划日期",type:"input",value:""},
            {prop:"TaskID",label:"制药任务单号",type:"input",value:""},
            {prop:"BatchID",label:"批次号",type:"input",value:""},
            {prop:"PlanSeq ",label:"顺序号",type:"input",value:""},
            {prop:"PUCode",label:"工艺段编码",type:"input",value:""},
            {prop:"PDUnitRouteName",label:"工艺路线名称",type:"input",value:""},
            {prop:"PlanType",label:"计划类型",type:"input",value:""},
            {prop:"BrandCode",label:"品名编码",type:"input",value:""},
            {prop:"BrandName",label:"牌号名称",type:"input",value:""},
            {prop:"PlanQuantity",label:"计划重量",type:"input",value:""},
            {prop:"ActQuantity",label:"实际重量",type:"input",value:""},
            {prop:"Unit",label:"单位",type:"input",value:""},
            {prop:"EnterTime",label:"录入时间",type:"input",value:""},
            {prop:"ActBeginTime",label:"实际开始时间",type:"input",value:""},
            {prop:"ActEndTime",label:"实际完成时间",type:"input",value:""},
            {prop:"SetRepeatCount",label:"设定重复次数",type:"input",value:""},
            {prop:"CurretnRepeatCount",label:"当前重复次数",type:"input",value:""},
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
      this.getPlanTable()
      this.getProcessTaskTable()
      this.getProcessPlanTable()
    },
    methods:{
      getPlanTable(){
        var that = this
        var params = {
          tableName: this.PlanTableData.tableName,
          limit:this.PlanTableData.limit,
          offset:this.PlanTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.PlanTableData.data = data.rows
            that.PlanTableData.total = data.total
          }
        },res =>{
          console.log("请求错误")
        }
        )
      },
      getProcessPlanTable(){
        var that = this
        var params = {
          tableName: this.ProcessPlanTableData.tableName,
          limit:this.ProcessPlanTableData.limit,
          offset:this.ProcessPlanTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.ProcessPlanTableData.data = data.rows
            that.ProcessPlanTableData.total = data.total
          }
        },res =>{
          console.log("请求错误")
        }
        )
      },
      getProcessTaskTable(){
        var that = this
        var params = {
          tableName: this.ProcessTaskTableData.tableName,
          limit:this.ProcessTaskTableData.limit,
          offset:this.ProcessTaskTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.ProcessTaskTableData.data = data.rows
            that.ProcessTaskTableData.total = data.total
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
