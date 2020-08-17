<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">工艺参数配置</span>
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
          tableName:"ProductParameter",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"PDParaCode",label:"产品段工艺参数编码",type:"input",value:""},
            {prop:"PDParaName",label:"产品段工艺参数名称",type:"input",value:""},
            {prop:"Desc",label:"描述",type:"input",value:""},
            {prop:"Value",label:"值",type:"input",value:""},
            {prop:"Unit",label:"单位",type:"input",value:""},
            {prop:"ProductRuleID",label:"产品定义ID",type:"Unit",value:""},
            {prop:"PUID",label:"工艺段ID",type:"Unit",value:""},
            {prop:"Seq",label:"顺序号",type:"Unit",value:""},
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