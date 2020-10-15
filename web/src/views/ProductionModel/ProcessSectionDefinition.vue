<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span>工艺段定义</span>
        <span class="text-size-12 color-grayblack marginLeft">维护所有生产工序</span>
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
    name: "ProcessSectionDefinition",
    components:{tableView},
    data(){
      return {
        PermissionTableData:{
          tableName:"ProcessUnit",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"PUCode",label:"工艺段编码",type:"input",value:""},
            {prop:"PUName",label:"工艺段名称",type:"input",value:""},
            {prop:"RelateTaskCount",label:" 相关任务数",type:"input",value:""},
            {prop:"PURunTime",label:" 工艺运行时长",type:"input",value:""},
            {prop:"PUWaitTime",label:" 工艺等待时长",type:"input",value:""},
            {prop:"Desc",label:"描述",type:"input",value:"",searchProp:false,canSubmit:false},
            {prop:"PURateCapacity",label:"额定生产能力",type:"input",value:"",searchProp:false,canSubmit:false},
            {prop:"PUPLanCapacity",label:"计划生产能力",type:"input",value:""},
            {prop:"CapacityUnit",label:"能力单位",type:"input",value:""},
            {prop:"PlaceTime",label:"静置时间",type:"input",value:""},
            {prop:"TimeUnit",label:"时间单位",type:"input",value:""},
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
