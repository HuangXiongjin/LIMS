<template>
  <el-row>
    <el-col>
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">产品工艺段参数</span>
      </div>
      <div class="platformContainer">
        <tableView :tableData="ProductParameterTableData" @getTableData="getProductParameterTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "ProductParameter",
    components:{tableView},
    data(){
      return {
        ProductParameterTableData:{
          tableName:"ProductParameter",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"PDParaCode",label:"工艺参数编码",type:"input",value:""},
            {prop:"PDParaName",label:"工艺参数名称",type:"input",value:""},
            {prop:"Value",label:"值",type:"input",value:""},
            {prop:"PUName",label:"工艺段名称",type:"input",value:""},
            {prop:"Desc",label:"描述",type:"input",value:""},
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
      this.getProductParameterTable()
    },
    methods:{
      getProductParameterTable(){
        var that = this
        var params = {
          tableName: this.ProductParameterTableData.tableName,
          limit:this.ProductParameterTableData.limit,
          offset:this.ProductParameterTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.ProductParameterTableData.data = data.rows
            that.ProductParameterTableData.total = data.total
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
