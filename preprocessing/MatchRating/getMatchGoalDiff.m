function [goalDiffMatrix]=getMatchGoalDiff(listMatrix,statMatrix,dateMatrix,matchList,matchPeriodStart,matchPeriodFinish)

[x,y]=size(listMatrix);
[n,m]=size(statMatrix);
resultMatrix=zeros(x,1);
for i=1:x
    counter=0;
    for j=n:-1:1
        
        if (datenum(dateMatrix{j},'dd.mm.yyyy')<datenum(matchPeriodStart,'dd.mm.yyyy'))
       
            addValue=0;
                if (strcmp(matchList{j,1},listMatrix{i})==1)
                    counter=counter+1;
                    addValue=statMatrix(j,1)-statMatrix(j,2);
                    if counter<7
                        resultMatrix(i)=resultMatrix(i)+addValue;
                    end
                elseif (strcmp(matchList{j,2},listMatrix{i})==1)
                    counter=counter+1;
                    addValue=statMatrix(j,2)-statMatrix(j,1);
                    if counter<7
                        resultMatrix(i)=resultMatrix(i)+addValue;
                    end
                end
      
        end
        
        
    end
    
    
end

goalDiffMatrix=resultMatrix;
end