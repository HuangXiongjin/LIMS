<template>
  <el-row>
    <el-col>
      <div class="page-title">
        <span style="margin-left: 10px;" class="text-size-normol">生产设备定义</span>
      </div>
      <div class="platformContainer">
        <tableView class="" :tableData="EquipmentTableData" @getTableData="getEquipmentTable"></tableView>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import tableView from '@/components/CommonTable'
  export default {
    name: "Equipment",
    components:{tableView},
    data(){
      return {
        EquipmentTableData:{
          tableName:"Equipment",
          column:[
            {label:"ID",prop:"ID",type:"input",value:"",disabled:true,showField:false,searchProp:false},
            {prop:"EQPCode",label:"设备编码",type:"input",value:""},
            {prop:"EQPName",label:"设备名称",type:"input",value:""},
            {prop:"PUCode",label:"工艺段编码",type:"input",value:""},
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
      this.getEquipmentTable()
    },
    methods:{
      getEquipmentTable(){
        var that = this
        var params = {
          tableName: this.EquipmentTableData.tableName,
          limit:this.EquipmentTableData.limit,
          offset:this.EquipmentTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.EquipmentTableData.data = data.rows
            that.EquipmentTableData.total = data.total
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
