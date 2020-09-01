<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">生产线定义</span>
      </div>
      <div class="platformContainer">
        <tableView :tableData="ProductLineTableData" @getTableData="getProductLineTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "ProductLineDefinition",
    components:{tableView},
    data(){
      return {
        ProductLineTableData:{
          tableName:"ProductLine",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"PLineCode",label:"生产线编码",type:"input",value:""},
            {prop:"PLineName",label:"生产线名称",type:"input",value:""},
            {prop:"AreaCode",label:"区域编码",type:"input",value:""},
            {prop:"AreaName",label:"区域名称",type:"input",value:""},
            {prop:"Desc",label:"描述",type:"input",value:""},
            {prop:"PLineCapacity",label:"产线能力",type:"input",value:""},
            {prop:"Unit",label:"单位",type:"input",value:""},
            {prop:"Seq",label:"计划类型",type:"input",value:""},
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
      this.getProductLineTable()
    },
    methods:{
      getProductLineTable(){
        var that = this
        var params = {
          tableName: this.ProductLineTableData.tableName,
          limit:this.ProductLineTableData.limit,
          offset:this.ProductLineTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.ProductLineTableData.data = data.rows
            that.ProductLineTableData.total = data.total
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
