<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">产品定义</span>
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
    name: "Permission",
    components:{tableView},
    data(){
      return {
        PermissionTableData:{
          tableName:"ProductRule",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"PRCode",label:"产品定义编码",type:"input",value:""},
            {prop:"PRName",label:" 产品定义名称",type:"input",value:""},
            {prop:"Version",label:"版本",type:"input",value:""},
            {prop:"Desc",label:"描述",type:"input",value:""},
            {prop:"Publish_date",label:"发布日期",type:"input",value:"",searchProp:false,canSubmit:false},
            {prop:"Appy_date",label:"使用日期",type:"input",value:"",searchProp:false,canSubmit:false},
            {prop:"IsUsed",label:"是否使用",type:"select",value:"",Downtable:'isFlag',showDownField:'Description'},//显示下拉框，显示是、否
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
