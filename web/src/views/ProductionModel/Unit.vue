<template>
  <el-row>
    <el-col>
      <div class="page-title">
        <span>产品单位定义</span>
      </div>
      <div class="platformContainer">
        <tableView :tableData="UnitTableData" @getTableData="getUnitTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "Unit",
    components:{tableView},
    data(){
      return {
        UnitTableData:{
          tableName:"Unit",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"UnitName",label:"单位名称",type:"input",value:""},
            {prop:"UnitValue",label:"单位值",type:"input",value:""},
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
      this.getUnitTable()
    },
    methods:{
      getUnitTable(){
        var that = this
        var params = {
          tableName: this.UnitTableData.tableName,
          limit:this.UnitTableData.limit,
          offset:this.UnitTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.UnitTableData.data = data.rows
            that.UnitTableData.total = data.total
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
