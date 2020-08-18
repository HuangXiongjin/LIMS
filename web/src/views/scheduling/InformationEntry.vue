<template>
  <el-row>
    <el-col :span="24">
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">排产计划录入</span>
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
          tableName:"product_plan",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"plan_period",label:"计划期间",type:"input",value:""},
            {prop:"product_code",label:"产品(即物料)编码",type:"input",value:""},
            {prop:"product_name",label:"产品(即物料)名称",type:"input",value:""},
            {prop:"product_unit",label:"计量单位 kg\批",type:"input",value:""},
            {prop:"meter_type",label:"计量类型 'B' 批次  'W'重量",type:"input",value:""},
            {prop:"bill_code",label:"单据号",type:"input",value:""},
            {prop:"plan_quantity",label:"计划数量",type:"input",value:""},
            {prop:"plan_type",label:"计划类型 'M' 月计划   'W'周计划",type:"input",value:""},
            {prop:"create_time",label:"插入时间",type:"input",value:""},
            {prop:"transform_time",label:"数据对接时间",type:"input",value:"",canSubmit:false,searchProp:false},
            {prop:"transform_flag",label:"数据对接MES 1 已对接 0 未对接",type:"input",value:"",canSubmit:false,searchProp:false},
            {prop:"Material_code",label:"物料编码",type:"input",value:""},
            {prop:"Material_name",label:"物料名称",type:"input",value:""},
            {prop:"Material_unit",label:"计量单位",type:"input",value:""},
            {prop:"Material_type",label:"物料类型",type:"input",value:""},
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
            // {type:"primary",label:"同步物料到WMS",clickEvent:'synchronizeToWMS'},
            // {type:"primary",label:"同步物料到备料段",clickEvent:'synchronizeToPrepareSection'},
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
      synchronizeToWMS(){
         alert('同步物料到WMS')
      },
      synchronizeToPrepareSection(){
         alert('同步物料到备料段')
      },

    }
  }
</script>

<style scoped>

</style>