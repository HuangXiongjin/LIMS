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
                <div class="fontWet titl" style="height:40px;lineHeight:30px;borderBottom:1px solid #ccc;">{{currentgoods}}模板</div>
                <div class="mgt24">
                    <el-upload
                        drag
                        accept=".doc,.docx"
                        :action="uploadUrl"
                        :file-list="fileList"
                        :on-success='SuccessEvent'
                        :on-error='SubmitError'
                        :on-preview='handlepreview'
                        :before-upload="handleBeforeUpload"
                        :on-remove='deleteUploaded'
                        multiple>
                        <i class="el-icon-upload"></i>
                        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                        <div class="el-upload__tip" slot="tip">只能上传.doc，.docx类型的文件</div>
                     </el-upload>
                </div>
            </el-col>
            <el-dialog title="表格详细信息" :visible.sync="dialogFormVisible">
                <table  cellspacing="1" cellpadding="0" border="0" v-html="filebyte"></table>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
                </div>
            </el-dialog>
        </el-col>
    </el-row>
</template>
<script>
import "mammoth/mammoth.browser.js";
import Mammoth from "mammoth";
var moment=require('moment')
export default {
    data(){
        return {
           dialogFormVisible:false,
           filebyte:'',
           FileName:'',
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
           currentgoods:'',//当前点击的物类
           batchTableData:{ //物料BOM
                data:[],
                limit: 10,//当前显示多少条
                offset: 1,//当前处于多少页
                total: 0,//总的多少页
            },
            uploadUrl:'',
            fileList:[],
            batchtableconfig:[{prop:'Product',label:"名称"},{prop:'Code',label:'物料编码'},{prop:'Uint',label:'单位',width:'60'},{prop:'IntoTime',label:'录入时间',width:'160'},{prop:'IntoUser',label:'录入人'},{prop:'AlterTime',label:'修改时间',width:160},{prop:'AlterUser',label:'修改人'},{prop:'StandwardDocument',label:'项目标准文档'}],//批次列表
            treeDom: [],//渲染的树
            defaultProps: {
                children: 'children',
                label: 'label'
            }
        }
    },
    created(){
        this.getTreeDom()
    },
    methods: {
        handlepreview(){
            this.dialogFormVisible=true
        },
        deleteUploaded(file, fileList){ 
            var params={ID:file.ID}
            this.$confirm('确定要删除该文件吗？', '温馨提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.axios.delete('/lims/GetFile',{params:params}).then((res) => {
                   if(res.data.code=='1000'){
                       this.$message({
                        type:'success',
                        message:'删除成功'
                    })
                    this.getUploadedFile()
                   }
                })
            }).catch(() => {
                this.$message({
                    type:'info',
                    message:'已取消删除'
                })
                this.getUploadedFile()
            })
        },
        handleBeforeUpload(file){
        let that = this
        var FileExt = file.name.replace(/.+\./, "");
        if (['doc', 'docx'].indexOf(FileExt.toLowerCase()) === -1){ 
          this.$message({ type: 'warning', message: '请上传后缀名为[doc,docx]的附件！' });
          return false; 
          }else{
            var reader = new FileReader();
            reader.readAsArrayBuffer(file)
            reader.onload=function(){
              Mammoth.convertToHtml({ arrayBuffer: reader.result }).then((res) => {
               that.filebyte=res.value
               that.FileName=file.name
              })
            }    
          }        
      },
        getUploadedFile(){
            var params={
                Product:this.currentgoods
            }
            this.axios.get('/lims/GetFile',{params:params}).then((res) => {
                var arr=res.data.data
                this.fileList=arr.map((item,index) => {
                    return {
                        name:item.FileName,
                        url:item.FilePath,
                        ID:item.ID
                    }
                })
            })
        },
        SubmitError(err, file, fileList){ //文件上传失败
            this.$message({
                type:'error',
                message:'上传失败，请重试'
            })
        },
        SuccessEvent(response, file, fileList){ //上传成功
            if(response.code=='1000'){
                this.$message({
                    type:'success',
                    message:'上传文件成功'
                })
                this.getUploadedFile()
            }
        },
        showTabInfo(obj,data,node){
            this.currentgoods=obj.label
            this.uploadUrl="/lims/Upload?Product="+obj.label
            this.getUploadedFile()
           //查询对应名字的数据
        },
        getTreeDom(){ //初始化获取树结构
            this.axios.get('/lims/Tree').then((res) => {
                if(res.data.code==='1000'){
                    this.treeDom=res.data.data
                }
            })
        }
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