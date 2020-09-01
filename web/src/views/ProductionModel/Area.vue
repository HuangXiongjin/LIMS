<template>
  <el-row>
    <el-col>
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">区域(车间)定义</span>
      </div>
      <div class="platformContainer">
        <tableView class="" :tableData="AreaTableData" @getTableData="getAreaTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "Area",
    components:{tableView},
    data(){
      return {
        AreaTableData:{
          tableName:"Area",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"AreaCode",label:"区域编码",type:"input",value:""},
            {prop:"AreaName",label:"区域名称",type:"input",value:""},
            {prop:"Desc",label:"描述",type:"input",value:""},
            {prop:"FactoryName",label:"所属厂区",type:"input",value:""},
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
      this.getAreaTable()
    },
    methods:{
      getAreaTable(){
        var that = this
        var params = {
          tableName: this.AreaTableData.tableName,
          limit:this.AreaTableData.limit,
          offset:this.AreaTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.AreaTableData.data = data.rows
            that.AreaTableData.total = data.total
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
