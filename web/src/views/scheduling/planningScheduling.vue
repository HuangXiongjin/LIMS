<template>
  <el-row :gutter='20'>
    <el-col :span='9'>
      <div>
        <div class="platformContainer" style="height:124px;">
          <div style="height:30px;lineHeight:30px;fontSize:16px;fontWeight:700;">计划明细</div>
            <div style="height:60px;lineHeight:70px;">
              <div style="display:inline-block;width:45%;">
                <div><span style="marginRight:15px;">当日计划数量</span><span>5批</span></div>
              </div>
              <div style="display:inline-block;width:45%;">
                <div><span style="marginRight:15px;">待处理计划数量</span><span>4批</span></div>
              </div>
            </div>
        </div>
        <div class="platformContainer" style="height:600px;overflow:auto;">
          <div style="height:40px;borderBottom:1px solid #ccc;fontSize:16px;fontWeight:700;">计划列表</div>
              <el-table
                  :data="sidetableData"
                  highlight-current-row
                  @row-click="handleCurrentChange"
                  style="width: 100%">
                   <el-table-column
                    type="index"
                    width="40">
                  </el-table-column>
                  <el-table-column v-for="item in tableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
              </el-table>
        </div>
      </div>
    </el-col>
    <el-col :span='15'>
      <BatchInformation :currentSBatch='currentFBatch'></BatchInformation>
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
         sidetableData: [{
            BatchID:'LPL20200825H',
            area: '新建综合制剂楼',
            date: '2016-05-02 08:00:00',
            status: '待执行'
          },{
            BatchID:'LCK20200825H',
            area: '固体制剂车间',
            date: '2016-05-03 12:00:00',
            status: '待执行'
          },{
            BatchID:'LCS20200825H',
            area: '前提取车间',
            date: '2016-05-05 18:00:00',
            status: '待执行'
          },
          {
            BatchID:'LCS20200825PL',
            area: '后提取车间',
            date: '2016-05-05 18:00:00',
            status: '待执行'
          },
          {
            BatchID:'LFGHH20200825H',
            area: '锅炉房',
            date: '2016-05-05 18:00:00',
            status: '待执行'
          }],
          mydata:[],
          currentFBatch:{},
          steps:[{title:'计划申请',decription:'开始时间 2020-09-10'},{title:'计划申请',decription:'开始时间 2020-09-10'},{title:'计划申请',decription:'开始时间 2020-09-10'}],
          tableconfig:[{prop:'BatchID',label:"生产批次",width:'90'},{prop:'area',label:'生产区域',width:'100'},{prop:'date',label:'生产日期',width:'190'},{prop:'status',label:'状态',width:'70'}],

      }
    },
    mounted(){
    },
    methods:{
      handleCurrentChange(e){
        this.currentFBatch=e
      }
    }
  }
</script>

<style scoped>

</style>
