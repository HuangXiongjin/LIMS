<template>
    <el-row :gutter='20'>
        <el-col :span='24' class="mgt24">
            <el-row>
                <el-col :span='3' class="mgr15 boxshadow">
                    <el-input
                        placeholder="类别/品名"
                        prefix-icon="el-icon-search"
                        v-model="searchObj.category">
                    </el-input>
                </el-col>
                <el-col :span='3' class="mgr15 boxshadow">
                    <el-select v-model="searchObj.goods" placeholder="物料类">
                        <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                        </el-option>
                    </el-select>
                </el-col>
                <el-col :span='3' class="mgr15 boxshadow">
                      <el-date-picker
                        v-model="searchObj.registrydate"
                        type="date"
                        placeholder="选择日期">
                      </el-date-picker>
                </el-col>
            </el-row>
        </el-col>
        <el-col :span='24' class="mgt24">
            <div class="container">
                <el-menu :default-active="'1'" class="bgwhite" mode="horizontal" @select="handleSelect">
                    <el-menu-item :index="'1'" style="height:46px;lineHeight:30px;">申请列表</el-menu-item>
                    <el-menu-item :index="'2'"  style="height:46px;lineHeight:30px;">申请通过清单</el-menu-item>
                </el-menu>
                <div class="mgt24" v-if="currentChoose==='1'">
                    <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%">
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                    </el-table>
                    <div class="paginationClass">
                        <el-pagination background  layout="total, prev, pager, next, jumper"
                        :total="batchTableData.total"
                        :current-page="batchTableData.offset"
                        :page-size="batchTableData.limit"
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange">
                        </el-pagination>
                    </div>
                </div>
                <div class="mgt24" v-if="currentChoose==='2'">
                    <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%">
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label'></el-table-column>
                    </el-table>
                    <div class="paginationClass">
                        <el-pagination background  layout="total, prev, pager, next, jumper"
                        :total="batchTableData.total"
                        :current-page="batchTableData.offset"
                        :page-size="batchTableData.limit"
                        @size-change="handleSizeChange"
                        @current-change="handleCurrentChange">
                        </el-pagination>
                    </div>
                </div>
            </div>
        </el-col>
    </el-row>
</template>
<script>
export default {
    data(){

        return {
           msg:'12',
           searchObj:{
               category:'',
               registrydate:'',
               goods:'',
           },
            options: [{
                value: '选项1',
                label: '物料一'
                }, {
                value: '选项2',
                label: '物料二'
                }],
            currentChoose:'1',
            batchTableData:{ //物料BOM
                tableName:"PlanManager",
                data:[],
                limit: 10,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchtableconfig:[{prop:'PlanNum',label:"计划单号"},{prop:'BatchID',label:'批次号'},{prop:'SchedulePlanCode',label:'调度编号'},{prop:'BrandCode',label:'品名编码'},{prop:'BrandName',label:'品名'},{prop:'BrandType',label:'产品类型'},{prop:'PlanQuantity',label:'计划产量'},{prop:'Unit',label:'单位'}],//批次列表
        }
    },
    created(){
        this.getPlanManager()
    },
    methods: {
        handleSelect(key) {
            this.currentChoose=key
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.getPlanManager()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.getPlanManager()
        },
        getPlanManager(){ //获取批次列表
        var params={
          tableName:'PlanManager',
          offset:this.batchTableData.offset-1,
          limit:this.batchTableData.limit
        }
        this.axios.get('/api/CUID',{params:params}).then(res => {
           if(res.data.code === "200"){
            var data = res.data.data
            this.batchTableData.data = data.rows
            this.batchTableData.total = data.total
          }
          },err=>{
            console.log("请求错误")
          })
      },
    },
}
</script>
<style scoped>

</style>