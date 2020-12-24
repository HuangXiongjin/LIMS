<template>
   <el-row :gutter="20">
        <el-col :span='5'>
            <el-col class="container" style="height:600px;overflow:auto;">
                <div class="fontWet titl">样本分类</div>
                <div style="marginTop:20px;">
                <el-tree
                    :data="treeDom"
                    node-key="id"
                    default-expand-all
                    :expand-on-click-node="false"
                    :props="defaultProps"
                    @node-click='showTabInfo'>
               </el-tree>
                </div>
            </el-col>
        </el-col>
        <el-col :span='19' class="container" style="height:600px;position:relative;">
            <el-col :span='24' class="mgt24">
                <div class="fontWet titl" style="height:40px;lineHeight:30px;borderBottom:1px solid #ccc;">{{currentgoods}}记录日志</div>
                <el-table
                    :data="batchTableData.data"
                    size='small'
                    highlight-current-row
                    style="width: 100%">
                    <el-table-column v-for="item in batchtableconfig" :key='item.prop' :prop='item.prop' :label='item.label' :width='item.width'></el-table-column>
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
            </el-col>
        </el-col>
    </el-row>
</template>
<script>
var moment=require('moment')
export default {
    data(){
        return {
           addEventdialogVisible: false,
           addEventForm:{
            categoryName: '',
            },
           MaterialForm:{ //新增输入框绑定
            Product: '',
            Code:'',
            Type:'',
            Source:'',
            Uint:'',
            IntoTime:'',
            IntoUser:'',
            AlterTime:moment(new Date()).format('YYYY-MM-DD HH:mm:ss'),
            AlterUser:localStorage.getItem('Name'),
            },
           materialdialogVisible:false, //新增物料信息卡片
           currentNodeData:{},//rename之后的保存
           currentParent:'',
           currentgoods:'玉米淀粉',//当前点击的物类
           ProductType:'辅料',
           batchTableData:{ 
                data:[],
                limit: 10,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            batchtableconfig:[{prop:'Product',label:"名称"},{prop:'CheckNumber',label:'请验单号'},{prop:'ProductType',label:'类型'},{prop:'Status',label:'操作'},{prop:'OperationTime',label:'操作时间',width:'180'},{prop:'User',label:'操作人'},{prop:'Work',label:'具体内容',width:'220'}],//批次列表
            treeDom: [],//渲染的树
            defaultProps: {
                children: 'children',
                label: 'label'
            }
        }
    },
    created(){
        this.getTreeDom()
        this.getTableData()
    },
    methods: {
        showTabInfo(obj,data,node){
          this.currentgoods=obj.label
          this.ProductType=data.parent.data.label
          this.getTableData()
        },
        getTableData(){
            var params={
               Page:this.batchTableData.offset,
               PerPage:this.batchTableData.limit,
               Product:this.currentgoods,
               ProductType:this.ProductType
           }
           this.axios.get('/lims/CheckLog',{params:params}).then((res) => {
               if(res.data.code=='1000'){
                   this.batchTableData.data=res.data.data
                   this.batchTableData.total=res.data.total
               }
           })
        },
        getTreeDom(){ //初始化获取树结构
            this.axios.get('/lims/Tree').then((res) => {
                if(res.data.code==='1000'){
                    this.treeDom=res.data.data
                }
            })
        },
        handleSizeChange(limit){ //每页条数切换
            this.batchTableData.limit = limit
            this.getTableData()
      },
        handleCurrentChange(offset) { // 页码切换
            this.batchTableData.offset = offset
            this.getTableData()
        },
    },
}
</script>
<style scoped>
    .operations{
        margin-left: 30px;
        position: absolute;
        right: 4px;
    }
    .el-tree-node__content{
        position: relative;
    }
</style>