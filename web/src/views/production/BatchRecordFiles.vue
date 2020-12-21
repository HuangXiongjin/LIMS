<template>
  <el-row :gutter="15">
    <el-col :span='24'>
      <div class="page-title"><span>选择工序维护批记录</span></div>
      <div>
          <el-tag class="marginBottom marginRight cursor-pointer" v-for="(item,index) in ProcessList" :key="index" v-bind:effect="item.PUName===PUName?'dark':'plain'" @click="showPGL(item.PUName,item.PUCode)">{{item.PUName}}</el-tag>
      </div>
      <div class='platformContainer' v-if="PUName">
        <el-upload
          class="marginBottom"
          drag
          accept=".doc,.docx"
          action="/api/batchmodelexport"
          :limit="1"
          :on-preview="handlePreview"
          :before-remove="beforeRemove"
          :before-upload="handleBeforeUpload"
          :on-remove="handleRemove"
          :on-exceed="handleExceed"
          :on-success='submitSuccess'
          :on-error='submitError'
          :file-list="fileList">
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
          <div slot="tip" class="el-upload__tip">只能上传.doc,.docx 批记录表</div>
        </el-upload>
        <el-button type="primary" @click="FileHTMLPreview" size='small' v-if='ButtonVisible'>转换并配置接口参数</el-button>
      </div>
      <div class="platformContainer" v-if="dialogTableVisible">
        <p class="marginBottom">转换后的批记录模板</p>
        <el-form :inline="true">
          <el-form-item label="添加数据类型：">
             <el-radio-group v-model="handleCellRadio" size="small">
              <el-radio-button label="品名"></el-radio-button>
              <el-radio-button label="批次号"></el-radio-button>
              <el-radio-button label="录入数据字段"></el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveEditField" size='small'>保存配置</el-button>
          </el-form-item>
        </el-form>
        <table class="elementTable" cellspacing="1" cellpadding="0" border="0" v-html="filebyte"></table>
        <el-dialog title="采集值" :visible.sync="collectDialogVisible" width="30%">
          <el-table :data="CollectTableData.data" border size="small" ref="multipleTableCollect" @selection-change="handleSelectionChangeCollect" @row-click="handleRowClickCollect">
            <el-table-column type="selection"></el-table-column>
            <el-table-column prop="collectName" label="字段描述"></el-table-column>
            <el-table-column prop="collectKey" label="采集字段"></el-table-column>
          </el-table>
          <span slot="footer" class="dialog-footer">
            <el-button type="primary" @click="saveCollectData">保 存</el-button>
          </span>
        </el-dialog>
      </div>
    </el-col>
  </el-row>
</template>

<script>
  import "mammoth/mammoth.browser.js";
  var mammoth = require("mammoth");
  export default {
    name: "BatchRecordFiles",
    data(){
      return {
        results:[],
        PUCode:'',
        PUName:'',
        ProcessList:[],
        fileList: [],
        FileName:'',
        scheduleTableData:[],
        filebyte:'',
        fileID:'',
        dialogTableVisible:false,
        ButtonVisible:false, //是否显示配置按钮
        handleCellRadio:"录入数据字段", //添加的数据类型
        collectDialogVisible:false, //显示采集列表的弹框
        CollectTableData:{
          data:[
            {collectName:"第一次煎煮第一个小时时间",collectKey:"time1_1"},
            {collectName:"第一次煎煮第一个小时参数",collectKey:"value1_1"},
            {collectName:"第一次煎煮第二个小时时间",collectKey:"time1_2"},
            {collectName:"第一次煎煮第二个小时参数",collectKey:"value1_2"},
          ],
          multipleSelection:[]
        },
        cellDom:"",
      }
    },
    created(){
      this.getProcessTab()
    },
    methods:{
      getProcessTab(){
        var params={
          tableName:'ProcessUnit'
        }
        this.axios.get('/api/CUID',{params:params}).then(res=>{
          this.ProcessList=res.data.data.rows
        })
      },
      //获取存取的字符
      FileHTMLPreview(){
        let that = this
        this.dialogTableVisible = true
        if(this.dialogTableVisible){
          this.$nextTick(function () {
            $(".elementTable").find("tbody").css("display","inline-table")
            $(".elementTable").find("td").each(function(){
              $(this).click(function(){
                if($(this).hasClass("isInput") || $(this).hasClass("collect")){
                  that.$confirm('此操作将删除已定义的字段, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                  }).then(() => {
                    $(this).attr('class','')
                    $(this).attr('title','')
                  }).catch(() => {
                    that.$message({
                      type: 'info',
                      message: '已取消删除'
                    });
                  });
                }else{
                  if(that.handleCellRadio === "录入数据字段"){
                    that.$prompt('请输入单元格所需录入数据的字段', '提示', {
                      confirmButtonText: '确定',
                      cancelButtonText: '取消',
                    }).then(({ value }) => {
                      if(value){
                        $(this).addClass("isInput")
                        $(this).attr("data-field",value)
                        $(this).attr("title",value)
                      }else{
                        that.$message({
                          type: 'info',
                          message: '不能为空'
                        });
                      }
                    }).catch(() => {
                      that.$message({
                        type: 'info',
                        message: '取消输入'
                      });
                    });
                  }else if(that.handleCellRadio === "采集数据字段"){
                    that.collectDialogVisible = true
                    that.cellDom = $(this)
                  }else if(that.handleCellRadio === "品名"){
                    $(this).addClass("collect")
                    $(this).attr("data-field","ProductName")
                    $(this).attr("title","品名")
                  }else if(that.handleCellRadio === "批次号"){
                    $(this).addClass("collect")
                    $(this).attr("data-field","BatchNo")
                    $(this).attr("title","批次号")
                  }
                }
              })
           })
          })
        }
      },
      saveEditField(){
        this.$confirm('是否保存当前已配置好的批记录模板?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var newHtml = $('.elementTable').html();
          var params = {
            tableName:"BatchModel",
            ID:this.fileID,
            Parameter:newHtml
          }
          this.axios.put("/api/CUID",this.qs.stringify(params)).then(res =>{
            if(res.data.code === "200"){
              this.$message({
                type: 'success',
                message: res.data.message
              });
            }else{
              this.$message({
                type: 'info',
                message: res.data.message
              });
            }
          },res =>{
            console.log("请求错误")
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消保存'
          });
        });
      },
      //点击文件列表中已上传的文件
      handlePreview(file){ //点击文件列表提示是否下载
         this.$confirm('是否下载该文件到本地?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          window.open("/api/ManualDownload?FileName="+file.name) //下载文件
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消下载'
          });
        });        
      },
      showPGL(PUName,PUCode){ //点击工艺按钮
        //发起请求获取当前工艺pgl
        this.PUName=PUName
        this.PUCode=PUCode
        var params={
          PUCode:this.PUCode
        }
        this.axios.get('/api/batchmodelselect',{params:params}).then((res) => {
          if(res.data.code==='200'){
            if(res.data.message.length!==0){
              this.ButtonVisible=true
              this.filebyte=res.data.message[0].Parameter
              this.fileID=res.data.message[0].ID
            }else{
              this.ButtonVisible=false
            }
            this.fileList=res.data.message.map(item=>{
              return {name:item.FileName,url:item.FilePath,ID:item.ID}
            })
          }else{
             this.$message({
              type: 'error',
              message: '获取批记录文档失败'
            });
          }
        })
      },
      handleExceed(files, fileList) {
          this.$message({
          message: '限制只能上传一条数据',
          type: 'error'
        });
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },
      //文件上传成功时的钩子
      submitSuccess(response, file, fileList){
        let that = this
        this.$message({
            message: "上传文件成功！",
            type: 'success'
        });
        var reader = new FileReader();
        reader.readAsArrayBuffer(file.raw)
        reader.onload=function(loadEvent){
          mammoth.convertToHtml({ arrayBuffer: loadEvent.target.result }).then(function(res){
            that.filebyte=res.value
            that.FileName=file.name
            that.filebyte = that.filebyte.replace(/□/g,'<input type="checkbox" value="0"/>')
            var params={
             PUCode:that.PUCode,
             PUIDName:that.PUName,
             FileName:that.FileName,
             Parameter:that.filebyte
            }
            that.axios.post('/api/batchmodelinsert',that.qs.stringify(params)).then((res) => {
              if(res.data.code==='200'){
                that.showPGL(that.PUName,that.PUCode)
              }
            })
          }).done()
        }
      },
      submitError(){
        this.$message({
          message:'上传失败，请重新上传文件',
          type:'error'
        })
      },
      //上传文件之前
      handleBeforeUpload(file){
        var FileExt = file.name.replace(/.+\./, "");
        if (['doc', 'docx'].indexOf(FileExt.toLowerCase()) === -1){ 
          this.$message({ type: 'warning', message: '请上传后缀名为[doc,docx]的附件！' });
          return false
        }
      },
      //文件列表移除文件
      handleRemove(file,fileList){
        var fileID=file.ID
        var params={
          id:fileID
        }
        this.axios.post('/api/ManualDelete',this.qs.stringify(params)).then((res) => {
          if(res.data.code==='200'){
             this.showPGL(this.PUName,this.PUCode,this.ActiveIndex)
          }
        })
      },
      handleSelectionChangeCollect(row){ //选择采集数据
        this.CollectTableData.multipleSelection = row
      },
      handleRowClickCollect(row){
        this.$refs.multipleTableCollect.clearSelection()
        this.$refs.multipleTableCollect.toggleRowSelection(row)
      },
      saveCollectData(){  //保存选择的采集值
        if(this.CollectTableData.multipleSelection.length == 1){
          this.cellDom.addClass("collect")
          this.cellDom.attr("data-field",this.CollectTableData.multipleSelection[0].collectKey)
          this.cellDom.attr("title",this.CollectTableData.multipleSelection[0].collectKey)
          this.collectDialogVisible = false
        }else{
          this.$message({
            message: "请选择一条采集字段！",
            type: 'info'
          });
        }
      }
    }
  }
</script>

<style scoped>
  .container-col{
    display: inline-block;
    clear: both;
    overflow: hidden;
    border:1px solid #228AD5;
    background:#fff;
    border-radius: 4px;
    padding: 0 15px;
    margin-bottom: 15px;
    margin-right: 10px;
    height: 40px;
    line-height: 40px;
    color: #000;
  }
  .pactive{
    background-color:#228AD5;
    color:#fff;
  }
</style>
