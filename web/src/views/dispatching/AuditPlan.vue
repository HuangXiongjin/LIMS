<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">审核计划</span>
      </div>
      <div class="platformContainer">
        <tableView class="" :tableData="PermissionTableData" @getTableData="getPermissionTable" @auditInformation='auditInformation'></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "ProductUnit",
    components:{tableView},
    data(){
      return {
        PermissionTableData:{
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
          dialogVisible: false,
          dialogTitle:'',
          handleType:[
            {type:"warning",label:"批量通过审核",clickEvent:'auditInformation',icon:'el-icon-s-check'},
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
      auditInformation(){
          alert('执行审核信息函数')
      }
    }
  }
</script>

<style scoped>

</style>
