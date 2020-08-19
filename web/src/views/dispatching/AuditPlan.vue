<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">产品段定义</span>
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
            {prop:"PDUnitCode",label:"产品段编码",type:"input",value:""},
            {prop:"PDUnitName",label:"产品段名称",type:"input",value:""},
            {prop:"Desc",label:"描述",type:"input",value:""},
            {prop:"Duration",label:"持续时间",type:"input",value:""},
            {prop:"LowLimit",label:"低限",type:"input",value:""},
            {prop:"HighLimit",label:"高限",type:"input",value:""},
            {prop:"RelateTaskCount",label:"相关任务数",type:"input",value:""},
            {prop:"ProductRuleID",label:"产品定义ID",type:"input",value:""},
            {prop:"PUID",label:"工艺段ID",type:"input",value:""},
            {prop:"Seq",label:"顺序号",type:"input",value:""},
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
