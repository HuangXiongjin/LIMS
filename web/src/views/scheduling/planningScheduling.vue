<template>
  <el-row :gutter='20'>
    <el-col :span='9'>
      <div>
        <div class="platformContainer" style="height:124px;">
            <div>计划状态选择</div>
            <div style="margin-top: 20px">
              <el-checkbox-group v-model="checkboxGroup" size="small">
                <el-checkbox-button v-for="city in cities" :label="city" :key="city">{{city}}</el-checkbox-button>
              </el-checkbox-group>
            </div>
        </div>
        <div class="platformContainer" style="height:900px;overflow:auto;">
          <div style="height:40px;borderBottom:1px solid #ccc;fontSize:16px;fontWeight:700;">计划列表</div>
              <el-table
                  :data="planTableData.data"
                  highlight-current-row
                  size='small'
                  @row-click="TabCurrentChange"
                  style="width: 100%">
                   <el-table-column
                    type="index"
                    width="40">
                  </el-table-column>
                  <el-table-column v-for="item in tableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
              </el-table>
              <div class="paginationClass">
                  <el-pagination background  layout="total,prev, pager, next, jumper"
                  :total="planTableData.total"
                  :current-page="planTableData.offset"
                  :page-size="planTableData.limit"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange">
                  </el-pagination>
            </div>
        </div>
      </div>
    </el-col>
    <el-col :span='15'>
      <BatchInformation :currentSBatch='currentFBatch' ref='BatchInfo'></BatchInformation>
    </el-col>
  </el-row>
</template>

<script>
import BatchInformation from '@/components/BatchInformatin.vue'
  export default {
    name: "planningScheduling",
    components:{BatchInformation},
    data(){
      return {
          planTableData:{
            tableName:"PlanManager",
            data:[],
            limit: 10,//当前显示多少条
            offset: 1,//当前处于多少页
            total: 0,//总的多少页
        },
          cities:['上海', '北京', '广州', '深圳'],
          checkboxGroup: ['上海'],
          BrandActive:'',
          mydata:[],
          currentFBatch:{},
          currentBrandName:'',
          tableconfig:[{prop:'BatchID',label:"批次号"},{prop:'BrandName',label:'品名'},{prop:'PlanStatus',label:'计划状态'}],
      }
    },
    created(){
      this.getBatchTable()
    },
    mounted(){
    },
    methods:{
      getBatchTable(){ //初始化获取表的内容
        var that = this
        var params = {
          tableName: this.planTableData.tableName,
          limit:this.planTableData.limit,
          offset:this.planTableData.offset - 1
        }
        this.axios.get("/api/CUID",{
          params: params
        }).then(res =>{
          if(res.data.code === "200"){
            var data = res.data.data
            that.planTableData.data = data.rows
            that.planTableData.total = data.total
          }
        },res =>{
          console.log("请求错误")
        }
        )
      },
      TabCurrentChange(e){ //点击显示当前的tab行显示详细信息
        this.currentFBatch=e
        this.currentBrandName=e.BrandName
        this.$refs.BatchInfo.getMaterialBom(this.currentBrandName)
      },
      handleSizeChange(limit){ //每页条数切换
        this.planTableData.limit = limit
        this.getBatchTable()
      },
       handleCurrentChange(offset) { // 页码切换
        this.planTableData.offset = offset
        this.getBatchTable()
      }
    }
  }
</script>

<style scoped>

</style>
