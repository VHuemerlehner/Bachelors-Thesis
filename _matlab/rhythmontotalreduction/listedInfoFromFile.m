function listedInfoFromFile(foldName, filName)

tmpF = sprintf('./data/%s/%s', foldName, filName);

fid = fopen(tmpF,'rt');
tmp = textscan(fid,'%s %f %s','Delimiter','\t');
fclose(fid);

d = cell(size(tmp{3},1),3);

for i = 1:size(tmp{3},1)
    
    d{i,1} = tmp{1}{i};
    d{i,2} = tmp{2}(i);
    d{i,3} = str2num(tmp{3}{i});
    
end

% read line by line

h = {'time','surface','reduction','melodyPC', 'melodyMIDI'};

tmpKey = 0;
tmpMode = [0, 2, 4, 5, 7, 9, 11];

tmpIdx = 2;
prevTime = -1;

for i = 1:size(d,1)
    
    currTime = d{i,2};
    
    if strcmp(d{i,1}, 'tonality')
        tmpKey = mod(d{i,3}(1), 12);
        tmpMode = mod(d{i,3} - tmpKey, 12);
        
        tmpIdx = tmpIdx + 1;
        
        h{tmpIdx, 1} = 'tonality';
        h{tmpIdx, 2} = tmpKey;
        h{tmpIdx, 3} = mat2str(tmpMode);
        h{tmpIdx, 4} = '-------';
        h{tmpIdx, 5} = '-------';
    elseif strcmp(d{i,1}, 'grouping')
        
        tmpIdx = tmpIdx + 1;
        
        h{tmpIdx, 1} = 'grouping';
        h{tmpIdx, 2} = currTime;
        h{tmpIdx, 3} = '-------';
        h{tmpIdx, 4} = '-------';
        h{tmpIdx, 5} = '-------';
    else
        if currTime ~= prevTime
            prevTime = currTime;
            tmpIdx = tmpIdx + 1;
        end
        h{tmpIdx, 1} = currTime;
        if strcmp(d{i,1}, 'surface')
            % h{tmpIdx, 2} = d{i,3};
            % h{tmpIdx, 4} = max(d{i,3});
            [r,t,x] = HARM_keyMergeConsRoot(...
                    d{i,3},...
                    tmpKey,...
                    tmpMode);
            tmpX = [t{1},x{1}];
            h{tmpIdx, 2} = mat2str([r{1},tmpX]);
%             h{tmpIdx, 2} = sprintf('[%d,_',r{1});
%             tmpX = [t{1},x{1}];
%             for j = 1:length(tmpX)
%                 h{tmpIdx, 2} = strcat(h{tmpIdx, 2}, sprintf('%d_',tmpX(j)));
%             end
%             h{tmpIdx, 2} = strcat(h{tmpIdx, 2}, ']');
            % h{tmpIdx, 4} = mod(max(d{i,3}) - tmpKey, 12);
        elseif strcmp(d{i,1}, 'reduction')
            % h{tmpIdx, 3} = d{i,3};
            [r,t,x] = HARM_keyMergeConsRoot(...
                    d{i,3},...
                    tmpKey,...
                    tmpMode);
            tmpX = [t{1},x{1}];
            h{tmpIdx, 3} = mat2str([r{1},tmpX]);
%             h{tmpIdx, 3} = sprintf('[%d,_',r{1});
%             tmpX = [t{1},x{1}];
%             for j = 1:length(tmpX)
%                 h{tmpIdx, 3} = strcat(h{tmpIdx, 3}, sprintf('%d_',tmpX(j)));
%             end
%             h{tmpIdx, 3} = strcat(h{tmpIdx, 3}, ']');
        else
            h{tmpIdx, 4} = mod(max(d{i,3}) - tmpKey, 12);
            h{tmpIdx, 5} = max(d{i,3});
        end
    end
    
end

cell2csv(strcat(filName,'.csv'), h, ';');
movefile(strcat(filName,'.csv'), sprintf('./output/%s',foldName));
    
end