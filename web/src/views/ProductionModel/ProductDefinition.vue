<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span>产品定义</span>
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
            {prop:"BrandCode",label:"产品编码",type:"input",value:""},
            {prop:"BrandName",label:" 产品名称",type:"input",value:""},
            {prop:"BrandType",label:" 产品类型",type:"input",value:""},
            {prop:"BatchWeight",label:" 批次重量",type:"input",value:""},
            {prop:"BatchTimeLength",label:" 批次时长",type:"input",value:""},
            {prop:"AvalProductLine",label:"可用生产线",type:"select",multiple:true,value:[],Downtable:'ProductLine',showDownField:'PLineName'},
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
