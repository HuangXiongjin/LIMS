<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span>产品定义</span>
      </div>
      <div class="platformContainer">
        <tableView class="" :tableData="PermissionTableData" @getTableData="getPermissionTable" @sendToWMS="sendToWMS"></tableView>
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
            {prop:"BrandCode",label:"产品编码",type:"input",value:""},
            {prop:"BrandName",label:" 产品名称",type:"input",value:""},
            {prop:"BrandType",label:" 产品类型",type:"input",value:""},
            {prop:"BatchWeight",label:" 批生产能力",type:"input",value:""},
            {prop:"Unit",label:" 单位",type:"input",value:""},
            {prop:"Version",label:"版本",type:"input",value:""},
            {prop:"Desc",label:"描述",type:"input",value:""},
            {prop:"SendFlag",label:"发送标识",disabled:true,type:"input",value:"",defaultValue:"待发送",dataJudge:[{color:"#168DD7",value:"已发送"},{color:"#FA7D00",value:"待发送"}]},
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
            {type:"primary",label:"发送到WMS",clickEvent:"sendToWMS"},
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
      sendToWMS(){
        if(this.PermissionTableData.multipleSelection.length > 0){
          var mulId = []
          var params = {}
          this.PermissionTableData.multipleSelection.forEach(item =>{
            mulId.push({id:item.ID});
          })
          params.sendData = JSON.stringify(mulId)
          this.$confirm('确定发送所选品名信息到WMS？', '提示', {
            distinguishCancelAndClose:true,
            type: 'warning'
          }).then(()  => {
            this.axios.post("/api/WMS_SendMatilInfo",this.qs.stringify(params)).then(res =>{
              if(res.data.code === "200"){
                this.$message({
                  type: 'success',
                  message: res.data.message
                });
              }
              this.getPermissionTable()
            },res =>{
              console.log("请求错误")
            })
          }).catch(() => {
            this.$message({
              type: 'info',
              message: '已取消发送'
            });
          });
        }else{
          this.$message({
            type: 'info',
            message: "请选择品名"
          });
        }
      },
    }
  }
</script>

<style scoped>

</style>
